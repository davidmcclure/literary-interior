

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession

import lint.corpus._
import pprint.pprintln


object WriteTextTest {

  def main(args: Array[String]) {

    val sc = new SparkContext
    val spark = SparkSession.builder.getOrCreate()
    import spark.implicits._

    val tokens = List(
      Token(token="t1", start=0, end=1, offset=0.1),
      Token(token="t2", start=1, end=2, offset=0.2),
      Token(token="t3", start=2, end=3, offset=0.3),
      Token(token="t4", start=3, end=4, offset=0.4)
    )

    val text = Text(
      identifier="1",
      title="Title",
      authorFirst="David",
      authorLast="McClure",
      year=2017,
      text="text",
      tokens=tokens
    )

    val ds = spark.createDataset(Seq(text))

    ds.show()
    sc.stop()

  }

}
