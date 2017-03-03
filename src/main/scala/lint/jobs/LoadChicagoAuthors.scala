

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.{SparkSession,SaveMode}

import lint.config.Config
import lint.corpora.chicago.AuthorCSV


object LoadChicagoAuthors extends Config {

  val sc = new SparkContext(new SparkConf)
  val spark = SparkSession.builder.getOrCreate()
  import spark.implicits._

  def main(args: Array[String]) {

    val authors = AuthorCSV.fromConfig.read
    val ds = spark.createDataset(authors)

    ds.write.mode(SaveMode.Overwrite)
      .parquet(config.chicago.authorParquet)

    ds.show

  }

}
