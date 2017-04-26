

package lint.jobs

import org.apache.spark.sql.{SparkSession,SaveMode,Dataset}

import lint.Config
import lint.corpus.Novel
import lint.corpus.NovelImplicits._


case class TokenOffsetsOpts(
  query: String = "",
  outPath: String = ""
)


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

    // Parse CLI args.
    val parser = new scopt.OptionParser[TokenOffsetsOpts]("offsets") {

      arg[String]("query")
        .action((x, c) => c.copy(query = x))
        .text("Query token")

      arg[String]("outPath")
        .action((x, c) => c.copy(outPath = x))
        .text("Output path")

    }

    val opts = parser.parse(args, TokenOffsetsOpts()).get

    val novels = spark.read
      .parquet(config.corpus.novelParquet)
      .as[Novel]

    // Query offset sequences.
    val offsets = ExtTokenOffsets.mergeOffsets(novels, opts.query)

    offsets.write.json(opts.outPath)

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
