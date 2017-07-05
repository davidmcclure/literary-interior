

package lint.jobs

import org.apache.spark.sql.{SparkSession,SaveMode,Dataset}

import lint.Config
import lint.corpus.Novel


case class TokenOffsetsOpts(
  query: String = "",
  outPath: String = ""
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
    val offsets = novels.map(_.tokenOffsets(opts.query))

    offsets.write.json(opts.outPath)

  }

}
