

package lint.jobs

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.{SparkSession,SaveMode}

import lint.config.Config
import lint.corpus.{Novel,TokenBin}
import lint.corpus.NovelImplicits._


// TODO|dev
case class Row(
  token: String,
  pos: String,
  bin: Int,
  count: Int
)


object ExtBinCounts extends Config {

  val sc = new SparkContext(new SparkConf)
  val spark = SparkSession.builder.getOrCreate()
  import spark.implicits._

  def main(args: Array[String]) {

    val novels = spark.read
      .parquet(config.corpus.novelParquet)
      .as[Novel]

    // TODO: test
    val counts = novels

      // Get list of (TokenBin, count)
      .flatMap(_.binCounts().toSeq)

      // Sum the counts for each key across all texts.
      .rdd.reduceByKey(_+_)

      // Merge into database rows.
      .map {
        case (tb: TokenBin, count: Int) =>
        Row(tb.token, tb.pos, tb.bin, count)
      }

    counts.toDF.show(100)

  }

}
