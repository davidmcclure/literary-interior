

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.{SparkSession,SaveMode}
import pprint.pprintln

import lint.config.Config
import lint.corpus.Novel


case class Opts(

  query: String = null,
  outPath: String = null,

  minOffset: Double = 0,
  maxOffset: Double = 100,
  //minYear: Double = 0,
  //maxYear: Double = 2000,
  sampleFraction: Double = 1

)


case class Match(
  corpus: String,
  identifier: String,
  title: String,
  authorFirst: Option[String],
  authorLast: Option[String],
  year: Int,
  offset: Double,
  snippet: String
)


object KWIC extends Config {

  val sc = new SparkContext(new SparkConf)
  val spark = SparkSession.builder.getOrCreate()
  import spark.implicits._

  def main(args: Array[String]) {

    // Define argument rules.
    val parser = new scopt.OptionParser[Opts]("kwic") {

      arg[String]("query")
        .action((x, c) => c.copy(query = x))
        .text("Query token")

      arg[String]("outPath")
        .action((x, c) => c.copy(outPath = x))
        .text("Output path")

      opt[Double]("minOffset")
        .action((x, c) => c.copy(minOffset = x))
        .text("Minimum 0-1 offset.")

      opt[Double]("maxOffset")
        .action((x, c) => c.copy(maxOffset = x))
        .text("Maximum 0-1 offset.")

      opt[Double]("sampleFraction")
        .action((x, c) => c.copy(sampleFraction = x))
        .text("Fraction of matches to sample.")

    }

    // Parse args.
    val opts = parser.parse(args, Opts()) match {
      case Some(args) => args
      case None => throw new Exception("Invalid args.")
    }

    // Read novels.
    val novels = spark.read
      .parquet(config.novelParquet)
      .as[Novel]

    // Probe for query matches.
    val matches = novels.flatMap(novel => {

      for (
        token <- novel.tokens
        if (token.token == opts.query)
        if (token.offset >= opts.minOffset)
        if (token.offset <= opts.maxOffset)
      ) yield {

        // TODO: Parametrize radius.
        val hit = novel.text.slice(token.start, token.end)
        val prefix = novel.text.slice(token.start-100, token.start)
        val suffix = novel.text.slice(token.end, token.end+100)

        val snippet = prefix + s"***${hit}***" + suffix

        Match(
          corpus=novel.corpus,
          identifier=novel.identifier,
          title=novel.title,
          authorFirst=novel.authorFirst,
          authorLast=novel.authorLast,
          year=novel.year,
          offset=token.offset,
          snippet=snippet
        )

      }

    })

    // Sample results.
    val sample = matches.sample(false, opts.sampleFraction)

    // Write single CSV.
    sample.coalesce(1).write
      .option("header", "true")
      .csv(opts.outPath)

  }

}
