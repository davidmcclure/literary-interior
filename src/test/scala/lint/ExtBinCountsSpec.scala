

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

    val d1 = for (_ <- (0 until 10).toList) yield {
      getNovel("corpus1", 1910, "one two three")
    }

    val d2 = for (_ <- (0 until 20).toList) yield {
      getNovel("corpus2", 1920, "four five six")
    }

    val d3 = for (_ <- (0 until 30).toList) yield {
      getNovel("corpus3", 1930, "seven eight nine")
    }

    val ds = spark.createDataset(d1 ++ d2 ++ d3)

    val rows = ExtBinCounts.mergeCounts(ds)

    val expected = Seq(

      BinCountRow("corpus1", 1910, "one", "CD", 0, 10),
      BinCountRow("corpus1", 1910, "two", "CD", 50, 10),
      BinCountRow("corpus1", 1910, "three", "CD", 99, 10),

      BinCountRow("corpus2", 1920, "four", "CD", 0, 20),
      BinCountRow("corpus2", 1920, "five", "CD", 50, 20),
      BinCountRow("corpus2", 1920, "six", "CD", 99, 20),

      BinCountRow("corpus3", 1930, "seven", "CD", 0, 30),
      BinCountRow("corpus3", 1930, "eight", "CD", 50, 30),
      BinCountRow("corpus3", 1930, "nine", "CD", 99, 30)

    )

    for (row <- expected) {
      rows.filter(_ == row).count shouldEqual 1
    }

  }

}
