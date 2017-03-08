

package lint.jobs

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.SparkSession
import org.scalatest._

import lint.tokenizer.Tokenizer
import lint.corpus.Novel


class ExtBinCountsMergeCountsSpec extends FlatSpec
  with Matchers with BeforeAndAfter {

  var spark: SparkSession = _

  before {

    val conf = new SparkConf()
      .setMaster("local[*]")
      .setAppName("test")

    spark = SparkSession.builder
      .config(conf)
      .getOrCreate()

  }

  after {
    spark.stop
  }

  // TODO: Scala equivalent of FactoryBoy?
  def getNovel(corpus: String, year: Int, text: String): Novel = {

    val tokens = Tokenizer.tokenize(text)

    Novel(
      corpus=corpus,
      identifier="1",
      title="title",
      authorFirst="first",
      authorLast="last",
      year=year,
      text=text,
      tokens=tokens
    )

  }

  "ExtBinCounts.mergeCounts" should "index TokenBin -> count" in {

    // TODO: Do this once?
    val spark_ = spark
    import spark_.implicits._

    val novels = for (i <- 0 until 10) yield {
      getNovel("corpus1", 1910, "one two three")
    }

    val ds = spark.createDataset(novels)

    ds.count shouldEqual 10

  }

}
