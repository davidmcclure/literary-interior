

package lindex.jobs

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.{SparkSession,SaveMode}

import lindex.config.Config
import lindex.corpora.chicago.AuthorCSV


object LoadChicagoAuthors extends Job with Config {

  import spark.implicits._

  def main(args: Array[String]) {

    val authors = AuthorCSV.fromConfig.read
    val ds = spark.createDataset(authors)

    ds.write.mode(SaveMode.Overwrite)
      .parquet(config.chicago.authorParquet)

    ds.show

  }

}
