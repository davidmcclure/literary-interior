

import org.apache.spark.sql.SparkSession

import lint.corpus._
import pprint.pprintln


object WriteTextTest {

  def main(args: Array[String]) {

    val spark = SparkSession.builder.getOrCreate()
    import spark.implicits._

    val text = Text.tokenize(
      identifier="1",
      title="Title",
      authorFirst="David",
      authorLast="McClure",
      year=2017,
      text="Does this work?"
    )

    val ds = spark.createDataset(Seq(text))

    ds.write.parquet("text.parquet")
    ds.show()

  }

}
