

package lint.jobs

import org.apache.spark.sql.{SparkSession,SaveMode,Dataset}

import lint.Config
import lint.corpus.Novel
import lint.corpus.NovelImplicits._


case class TokenOffsetsRow(
  corpus: String,
  identifier: String,
  title: String,
  year: Int,
  offsets: Seq[Double]
)


object ExtTokenOffsets extends Config {

  lazy val spark = SparkSession.builder.getOrCreate()
  import spark.implicits._

  def main(args: Array[String]) {

    val novels = spark.read
      .parquet(config.corpus.novelParquet)
      .as[Novel]

  }

  /* Merge together token / bin counts for novels.
   */
  def mergeOffsets(
    novels: Dataset[Novel],
    query: String
  ): Dataset[TokenOffsetsRow] = {

    novels.map { case n: Novel =>
      val offsets = n.tokenOffsets(query)
      TokenOffsetsRow(n.corpus, n.identifier, n.title, n.year, offsets)
    }

  }

}
