

package lint.jobs

import org.apache.spark.sql.{SparkSession,SaveMode}

import lint.Config
import lint.chicago.Loader


object LoadChicagoNovels extends Config {

  lazy val spark = SparkSession.builder.getOrCreate()
  import spark.implicits._

  def main(args: Array[String]) {

    val novels = spark
      .sparkContext
      .parallelize(Loader.sources)
      .map(Loader.parse)

    val ds = spark.createDataset(novels)

    ds.write.mode(SaveMode.Overwrite)
      .parquet(config.chicago.novelParquet)

  }

}
