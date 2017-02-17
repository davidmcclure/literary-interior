

import org.apache.spark.sql.SparkSession

import lint.corpus._
import pprint._


object ReadTexts {

  def main(args: Array[String]) {

    val spark = SparkSession.builder.getOrCreate()
    import spark.implicits._

    val texts = spark.read.parquet("text.parquet").as[Text]

    pprintln(texts.head.tokens)

  }

}
