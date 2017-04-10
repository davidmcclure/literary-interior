

package lint.jobs

import org.scalatest._
import org.scalatest.prop.TableDrivenPropertyChecks
import org.scalatest.prop.TableDrivenPropertyChecks._

import lint.tokenizer.Tokenizer
import lint.corpus.NovelFactory
import lint.test.helpers.SparkTestSession


class ExtBinCountsMergeCountsSpec extends FlatSpec with Matchers
  with SparkTestSession with TableDrivenPropertyChecks {

  "ExtBinCounts.mergeCounts" should "index TokenBin -> count" in {

    val spark = _spark
    import spark.implicits._

    val d1 = for (_ <- (0 until 10).toList) yield {
      NovelFactory(corpus="corpus1", year=1910, text="one two three")
    }

    val d2 = for (_ <- (0 until 20).toList) yield {
      NovelFactory(corpus="corpus2", year=1920, text="four five six")
    }

    val d3 = for (_ <- (0 until 30).toList) yield {
      NovelFactory(corpus="corpus3", year=1930, text="seven eight nine")
    }

    val ds = spark.createDataset(d1 ++ d2 ++ d3)

    val rows = ExtBinCounts.mergeCounts(ds)

    forAll(Table(

      ("corpus", "year", "token", "pos", "bin", "count"),

      // 10 in 1910
      ("corpus1",  1910, "one",   "CD", 0,  10),
      ("corpus1",  1910, "two",   "CD", 50, 10),
      ("corpus1",  1910, "three", "CD", 99, 10),

      // 20 in 1920
      ("corpus2",  1920, "four",  "CD", 0,  20),
      ("corpus2",  1920, "five",  "CD", 50, 20),
      ("corpus2",  1920, "six",   "CD", 99, 20),

      // 30 in 1930
      ("corpus3",  1930, "seven", "CD", 0,  30),
      ("corpus3",  1930, "eight", "CD", 50, 30),
      ("corpus3",  1930, "nine",  "CD", 99, 30)

    )) { (
      corpus: String,
      year: Int,
      token: String,
      pos: String,
      bin: Int,
      count: Int
    ) =>

      val row = BinCountRow(corpus, year, token, pos, bin, count)
      rows.filter(_ == row).count shouldEqual 1

    }

  }

  it should "round years to the nearest decade" in {

    val spark = _spark
    import spark.implicits._

    val ds = spark.createDataset(Seq(
      NovelFactory(corpus="corpus", year=1904, text="one two three"),
      NovelFactory(corpus="corpus", year=1905, text="one two three"),
      NovelFactory(corpus="corpus", year=1906, text="one two three")
    ))

    val rows = ExtBinCounts.mergeCounts(ds)

    forAll(Table(

      ("corpus", "year", "token", "pos", "bin", "count"),

      // 1904 -> 1900
      ("corpus", 1900, "one",   "CD", 0,  1),
      ("corpus", 1900, "two",   "CD", 50, 1),
      ("corpus", 1900, "three", "CD", 99, 1),

      // 1905 + 1906 -> 1910
      ("corpus", 1910, "one",   "CD", 0,  2),
      ("corpus", 1910, "two",   "CD", 50, 2),
      ("corpus", 1910, "three", "CD", 99, 2)

    )) { (
      corpus: String,
      year: Int,
      token: String,
      pos: String,
      bin: Int,
      count: Int
    ) =>

      val row = BinCountRow(corpus, year, token, pos, bin, count)
      rows.filter(_ == row).count shouldEqual 1

    }

  }

}
