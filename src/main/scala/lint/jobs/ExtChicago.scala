

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.{SparkSession,SaveMode}

import lint.chicago.Loader


object ExtChicago {

  val sc = new SparkContext(new SparkConf)
  val spark = SparkSession.builder.getOrCreate()
  import spark.implicits._

  def main(args: Array[String]) {

    val novels = sc
      .parallelize(Loader.sources)
      .map(Loader.parse)

    val ds = spark.createDataset(novels)

    ds.write.mode(SaveMode.Overwrite).parquet("chicago.parquet")

    ds.show()

  }

}

