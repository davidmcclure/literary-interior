

package lint.jobs

import org.apache.spark.sql.SparkSession

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

}
