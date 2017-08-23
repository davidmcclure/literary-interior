

package lint.jobs

import org.apache.spark.sql.{SparkSession,SaveMode,Dataset}

import lint.Config
import lint.corpus.{Novel,Ngram,NgramToken}


case class NgramRow(
  binCount: Int,
  bin: Int,
  tokens: Seq[NgramToken],
  count: Int
)


object ExtNgramBinCounts extends Config {

  lazy val spark = SparkSession.builder.getOrCreate()
  import spark.implicits._

  def main(args: Array[String]) {

    val novels = spark.read
      .parquet(config.corpus.novelParquet)
      .as[Novel]

    val counts = ExtNgramBinCounts.mergeCounts(novels)

    counts.write.mode(SaveMode.Overwrite)
      .json(config.corpus.ngramBinCountJSON)

  }

  /* Merge together counts for novels.
   */
  def mergeCounts(novels: Dataset[Novel]): Dataset[NgramRow] = {

    novels

      // 1-3 grams.
      .flatMap { novel =>
        (1 to 3).flatMap { order =>
          novel.ngramBinCounts(order).toSeq
        }
      }

      // Sum the counts for each key across all texts.
      .rdd.reduceByKey(_+_)

      // Merge bins and counts.
      .map { case (ng: Ngram, count: Int) =>
        NgramRow(
          ng.binCount,
          ng.bin,
          ng.tokens,
          count
        )
      }

      // Cast back to dataset.
      .toDS

  }

}
