

package lint.jobs

import org.apache.spark.sql.{SparkSession,SaveMode,Dataset}

import lint.Config
import lint.corpus.{Novel,Ngram1}


case class Ngram1Row(
  corpus: String,
  year: Int,
  bin: Int,
  token: String,
  pos: String,
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
  def mergeCounts(novels: Dataset[Novel]): Dataset[Ngram1Row] = {

    novels

      // Get list of (Ngram1, count)
      .flatMap(_.ngram1BinCounts(yearInterval=10).toSeq)

      // Sum the counts for each key across all texts.
      .rdd.reduceByKey(_+_)

      // Merge bins and counts.
      .map { case (ng: Ngram1, count: Int) =>
        Ngram1Row(ng.corpus, ng.year, ng.bin, ng.token, ng.pos, count)
      }

      // Cast back to dataset.
      .toDS

  }

}
