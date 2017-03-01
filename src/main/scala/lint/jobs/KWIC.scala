

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.{SparkSession,SaveMode}
import pprint.pprintln

import lint.config.Config
import lint.corpus.Novel


case class Args(

  // TODO: Don't give defaults?
  query: String = "query",
  outPath: String = "query.csv",

  minOffset: Double = 0,
  maxOffset: Double = 100,
  minYear: Double = 0,
  maxYear: Double = 2000

)


object KWIC extends Config {

  val sc = new SparkContext(new SparkConf)
  val spark = SparkSession.builder.getOrCreate()
  import spark.implicits._

  def main(args: Array[String]) {

    // Define argument rules.
    val parser = new scopt.OptionParser[Args]("kwic") {

      arg[String]("query")
        .action((x, c) => c.copy(query = x))
        .text("Query token.")

      arg[String]("outPath")
        .action((x, c) => c.copy(outPath = x))
        .text("Output path.")

    }

    // Parse args.
    val cliArgs = parser.parse(args, Args()) match {
      case Some(args) => args
      case None => throw new Exception("Invalid args.")
    }

    val novels = spark.read
      .parquet(config.novelParquet)
      .as[Novel]

    val matches = novels.flatMap(novel => {

      for (
        token <- novel.tokens
        if (token.token == cliArgs.query)
      ) yield {

        pprintln(token)
        token

      }

    })

    matches.show

  }

}
