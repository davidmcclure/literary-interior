

package lint.jobs

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.{SparkSession,SaveMode}

import lint.config.Config
import lint.corpus.Novel


object ExtBinCounts extends Config {

  val sc = new SparkContext(new SparkConf)
  val spark = SparkSession.builder.getOrCreate()
  import spark.implicits._

  def main(args: Array[String]) {

    val counts = spark.read
      .parquet(config.corpus.novelParquet)
      .as[Novel]
      .flatMap(_.binCounts().toSeq)
      .rdd
      .reduceByKey(_+_)

    counts.toDF.show(100)

  }

}
