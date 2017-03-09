

package lint.jobs

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.SparkSession
import org.scalatest._
import pprint.pprintln

import lint.tokenizer.Tokenizer
import lint.corpus.Novel


class ExtBinCountsMergeCountsSpec extends FlatSpec
  with Matchers with BeforeAndAfterAll {

  // TODO: Break into trait.

  var _spark: SparkSession = _

  override def beforeAll {

    val conf = new SparkConf()
      .setMaster("local[*]")
      .setAppName("test")

    _spark = SparkSession.builder
      .config(conf)
      .getOrCreate()

  }

  override def afterAll {
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

    for (row <- Seq(
      BinCountRow("corpus1", 1910, "one",   "CD", 0,  10),
      BinCountRow("corpus1", 1910, "two",   "CD", 50, 10),
      BinCountRow("corpus1", 1910, "three", "CD", 99, 10),
      BinCountRow("corpus2", 1920, "four",  "CD", 0,  20),
      BinCountRow("corpus2", 1920, "five",  "CD", 50, 20),
      BinCountRow("corpus2", 1920, "six",   "CD", 99, 20),
      BinCountRow("corpus3", 1930, "seven", "CD", 0,  30),
      BinCountRow("corpus3", 1930, "eight", "CD", 50, 30),
      BinCountRow("corpus3", 1930, "nine",  "CD", 99, 30)
    )) {
      rows.filter(_ == row).count shouldEqual 1
    }

  }

  it should "round years to the nearest decade" in {

    val spark = _spark
    import spark.implicits._

    val ds = spark.createDataset(Seq(
      getNovel("corpus", 1904, "one two three"),
      getNovel("corpus", 1905, "one two three"),
      getNovel("corpus", 1906, "one two three")
    ))

    val rows = ExtBinCounts.mergeCounts(ds)
    rows.show

    for (row <- Seq(
      BinCountRow("corpus", 1900, "one",   "CD", 0,  1),
      BinCountRow("corpus", 1900, "two",   "CD", 50, 1),
      BinCountRow("corpus", 1900, "three", "CD", 99, 1),
      BinCountRow("corpus", 1910, "one",   "CD", 0,  2),
      BinCountRow("corpus", 1910, "two",   "CD", 50, 2),
      BinCountRow("corpus", 1910, "three", "CD", 99, 2)
    )) {
      rows.filter(_ == row).count shouldEqual 1
    }

  }

}
