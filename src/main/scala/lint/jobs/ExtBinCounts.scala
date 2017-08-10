

package lint.jobs

import org.apache.spark.sql.{SparkSession,SaveMode,Dataset}

import lint.Config
import lint.corpus.{Novel,Unigram}


case class UnigramRow(
  corpus: String,
  year: Int,
  bin: Int,
  token: String,
  pos: String,
  count: Int
)


object ExtUnigramBinCounts extends Config {

  lazy val spark = SparkSession.builder.getOrCreate()
  import spark.implicits._

  def main(args: Array[String]) {

    val novels = spark.read
      .parquet(config.corpus.novelParquet)
      .as[Novel]

    val counts = ExtUnigramBinCounts.mergeCounts(novels)

    counts.write.mode(SaveMode.Overwrite)
      .json(config.corpus.unigramBinCountJSON)

  }

  /* Merge together token / bin counts for novels.
   */
  def mergeCounts(novels: Dataset[Novel]): Dataset[UnigramRow] = {

    novels

      // Get list of (Unigram, count)
      .flatMap(_.unigramBinCounts(yearInterval=10).toSeq)

      // Sum the counts for each key across all texts.
      .rdd.reduceByKey(_+_)

      // Merge bins and counts.
      .map { case (ng: Unigram, count: Int) =>
        UnigramRow(
          ng.corpus,
          ng.year,
          ng.bin,
          ng.token,
          ng.pos,
          count
        )
      }

      // Cast back to dataset.
      .toDS

  }

}
