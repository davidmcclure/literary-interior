

package lint.jobs

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.SparkSession
import org.scalatest._
import pprint.pprintln

import lint.tokenizer.Tokenizer
import lint.corpus.Novel


class ExtBinCountsMergeCountsSpec extends FlatSpec
  with Matchers with BeforeAndAfter {

  var _spark: SparkSession = _

  before {

    val conf = new SparkConf()
      .setMaster("local[*]")
      .setAppName("test")

    _spark = SparkSession.builder
      .config(conf)
      .getOrCreate()

  }

  after {
    _spark.stop
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

    // TODO: Any way to just do this once?
    val spark = _spark
    import spark.implicits._

    val novels = (0 until 10).flatMap(i => Seq(
      getNovel("corpus1", 1910, "one two three"),
      getNovel("corpus2", 1920, "four five six"),
      getNovel("corpus3", 1930, "seven eight nine")
    ))

    val ds = spark.createDataset(novels)

    val rows = ExtBinCounts.mergeCounts(ds)

    val expected = Seq(

      BinCountRow("corpus1", 1910, "one", "CD", 0, 10),
      BinCountRow("corpus1", 1910, "two", "CD", 50, 10),
      BinCountRow("corpus1", 1910, "three", "CD", 99, 10),

      BinCountRow("corpus2", 1920, "four", "CD", 0, 10),
      BinCountRow("corpus2", 1920, "five", "CD", 50, 10),
      BinCountRow("corpus2", 1920, "six", "CD", 99, 10),

      BinCountRow("corpus3", 1930, "seven", "CD", 0, 10),
      BinCountRow("corpus3", 1930, "eight", "CD", 50, 10),
      BinCountRow("corpus3", 1930, "nine", "CD", 99, 10)

    )

    for (row <- expected) {
      rows.filter(_ == row).count shouldEqual 1
    }

  }

}
