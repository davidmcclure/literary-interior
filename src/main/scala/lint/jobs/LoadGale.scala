

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.{SparkSession,SaveMode}
import scala.util.{Try,Success,Failure}

import lint.gale.Loader
import lint.config.Config


object LoadGale extends Config {

  // TODO: DRY this up?
  val sc = new SparkContext(new SparkConf)
  val spark = SparkSession.builder.getOrCreate()
  import spark.implicits._

  def main(args: Array[String]) {

    val novels = sc

      // Parse sources.
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

    ds.show

  }

}
