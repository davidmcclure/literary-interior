

package lint.jobs

import java.lang.Math

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.{SparkSession,SaveMode,Dataset}

import lint.Config
import lint.corpus.{Novel,TokenBin}
import lint.corpus.NovelImplicits._


case class BinCountRow(
  corpus: String,
  year: Int,
  token: String,
  pos: String,
  bin: Int,
  count: Int
)


object ExtBinCounts extends Config {

  lazy val spark = SparkSession.builder.getOrCreate()
  import spark.implicits._

  def main(args: Array[String]) {

    val novels = spark.read
      .parquet(config.corpus.novelParquet)
      .as[Novel]

    val counts = ExtBinCounts.mergeCounts(novels)

    counts.write.mode(SaveMode.Overwrite)
      .json(config.corpus.binCountJSON)

  }

  /* Merge together token / bin counts for novels.
   */
  def mergeCounts(novels: Dataset[Novel]): Dataset[BinCountRow] = {

    novels

      // Get list of (TokenBin, count)
      .flatMap(_.binCounts(yearInterval=10).toSeq)

      // Sum the counts for each key across all texts.
      .rdd.reduceByKey(_+_)

      // Merge bins and counts.
      .map { case (tb: TokenBin, count: Int) => {
        BinCountRow(tb.corpus, tb.year, tb.token, tb.pos, tb.bin, count)
      }}

      // Cast back to dataset.
      .toDS

  }

}
