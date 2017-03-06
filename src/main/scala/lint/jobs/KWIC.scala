

package lint.jobs

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.SparkSession

import lint.config.Config
import lint.corpus.Novel
import lint.corpus.NovelImplicits._


case class KWICOpts(
  query: String = "",
  outPath: String = "",
  minOffset: Double = 0,
  maxOffset: Double = 100,
  minYear: Double = 0,
  maxYear: Double = 3000,
  radius: Int = 100,
  fraction: Double = 1
)


object KWIC extends Config {

  val sc = new SparkContext(new SparkConf)
  val spark = SparkSession.builder.getOrCreate()
  import spark.implicits._

  /* Probe for KWICs, dump results to CSV.
   */
  def main(args: Array[String]) {

    // Define argument rules.
    val parser = new scopt.OptionParser[KWICOpts]("kwic") {

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

      opt[Int]("radius")
        .action((x, c) => c.copy(radius = x))
        .text("Snippet character radius.")

      opt[Double]("fraction")
        .action((x, c) => c.copy(fraction = x))
        .text("Fraction of matches to sample.")

    }

    // Parse args.
    val opts = parser.parse(args, KWICOpts()).get

    // Read novels.
    val novels = spark.read
      .parquet(config.corpus.novelParquet)
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
      opts.radius
    ))

    // Sample results.
    val sample = matches.sample(false, opts.fraction)

    // Write single JSON.
    sample.coalesce(1).write.json(opts.outPath)

  }

}
