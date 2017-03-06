

package lint.jobs

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.{SparkSession,SaveMode,Dataset}

import lint.config.Config
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

  val sc = new SparkContext(new SparkConf)
  val spark = SparkSession.builder.getOrCreate()
  import spark.implicits._

  def main(args: Array[String]) {

    val novels = spark.read
      .parquet(config.corpus.novelParquet)
      .as[Novel]

    val counts = ExtBinCounts.mergeCounts(novels)

    counts.coalesce(1).write
      .mode(SaveMode.Overwrite)
      .option("header", "true")
      .csv(config.corpus.binCountCSV)

    counts.show(100)

  }

  /* Merge together token / bin counts for novels.
   * TODO: test
   */
  def mergeCounts(novels: Dataset[Novel]): Dataset[BinCountRow] = {

    novels

      // Get list of (TokenBin, count)
      .flatMap(_.binCounts().toSeq)

      // Sum the counts for each key across all texts.
      .rdd.reduceByKey(_+_)

      // Merge into database rows.
      .map {
        case (tb: TokenBin, count: Int) => BinCountRow(
          tb.corpus,
          tb.year,
          tb.token,
          tb.pos,
          tb.bin,
          count
        )
      }

      // Cast back to dataset.
      .toDS

  }

}
