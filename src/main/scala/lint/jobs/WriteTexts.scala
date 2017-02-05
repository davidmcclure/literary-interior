

import org.apache.spark.sql.SparkSession

import lint.text._


object WriteTexts {

  def main(args: Array[String]) {

    val spark = SparkSession.builder.getOrCreate()
    import spark.implicits._

    val texts = for (i <- 0 to 1000) yield {

      Text(
        corpus="chicago",
        identifier=i.toString,
        title=s"Title${i}",
        authorFirst=s"David${i}",
        authorLast=s"McClure${i}",
        year=2000+i,
        text="Does this work?"
      )

    }

    val ds = spark.createDataset(texts)

    ds.write.parquet("text.parquet")
    ds.show()

  }

}
