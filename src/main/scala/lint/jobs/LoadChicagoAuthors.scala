

package lint.jobs

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.{SparkSession,SaveMode}

import lint.Config
import lint.chicago.AuthorCSV


object LoadChicagoAuthors extends Config {

  lazy val spark = SparkSession.builder.getOrCreate()
  import spark.implicits._

  def main(args: Array[String]) {

    val authors = AuthorCSV.fromConfig.read
    val ds = spark.createDataset(authors)

    ds.write.mode(SaveMode.Overwrite)
      .parquet(config.chicago.authorParquet)

  }

}
