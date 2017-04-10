

package lint.jobs

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.{SparkSession,SaveMode}
import scala.util.{Try,Success,Failure}

import lint.Config
import lint.gale.Loader


object LoadGale extends Config {

  lazy val spark = SparkSession.builder.getOrCreate()
  import spark.implicits._

  def main(args: Array[String]) {

    val novels = spark

      // Parse sources.
      .sparkContext
      .parallelize(Loader.sources)
      .map(s => Try(Loader.parse(s)))

      // Log + prune errors.
      .filter {
        case Success(v) => true
        case Failure(e) => println(e); false;
      }

      // Get results.
      .map(_.get)

    val ds = spark.createDataset(novels)

    ds.write.mode(SaveMode.Overwrite)
      .parquet(config.gale.novelParquet)

  }

}
