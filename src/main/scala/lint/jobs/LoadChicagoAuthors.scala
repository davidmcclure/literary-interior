

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.{SparkSession,SaveMode}

import lint.chicago.AuthorCSV


object LoadChicagoAuthors {

  val sc = new SparkContext(new SparkConf)
  val spark = SparkSession.builder.getOrCreate()
  import spark.implicits._

  def main(args: Array[String]) {

    val authors = AuthorCSV.fromConfig.read
    val ds = spark.createDataset(authors)

    // TODO: Config path.
    ds.write.mode(SaveMode.Overwrite).parquet("chicago-authors.parquet")
    ds.show()

  }

}
