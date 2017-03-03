

package lint.jobs.kwic

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.{SparkSession,SaveMode}
import pprint.pprintln

import lint.config.Config
import lint.corpus.Novel


case class Opts(
  query: String = "",
  outPath: String = "",
  minOffset: Double = 0,
  maxOffset: Double = 100,
  minYear: Double = 0,
  maxYear: Double = 3000,
  sampleFraction: Double = 1,
  snippetRadius: Int = 100
)


object KWIC extends Config {

  val sc = new SparkContext(new SparkConf)
  val spark = SparkSession.builder.getOrCreate()
  import spark.implicits._

  /* Probe for KWICs, dump results to CSV.
   */
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

      opt[Int]("minYear")
        .action((x, c) => c.copy(minYear = x))
        .text("Minimum year.")

      opt[Int]("maxYear")
        .action((x, c) => c.copy(maxYear = x))
        .text("Maximum year.")

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

      // Filter by year.
      .filter(n => {
        n.year >= opts.minYear &&
        n.year <= opts.maxYear
      })

    // Probe for query matches.
    val matches = novels.flatMap(novel => novel.kwic(
      opts.query,
      opts.minOffset,
      opts.maxOffset,
      opts.snippetRadius
    ))

    // Sample results.
    val sample = matches.sample(false, opts.sampleFraction)

    // Write single JSON.
    sample.coalesce(1).write.json(opts.outPath)

  }

}
