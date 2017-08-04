

package lint.jobs

import org.scalatest._
import org.scalatest.prop.TableDrivenPropertyChecks
import org.scalatest.prop.TableDrivenPropertyChecks._

import lint.utils.Tokenize
import lint.corpus.NovelFactory
import lint.test.helpers.SparkTestSession


class ExtBinCountsMergeCountsSpec extends FlatSpec with Matchers
  with SparkTestSession with TableDrivenPropertyChecks {

  "ExtBinCounts.mergeCounts" should "index Ngram1 -> count" in {

    val spark = _spark
    import spark.implicits._

    // 10 in 1910
    val d1 = for (_ <- (0 until 10).toList) yield {
      NovelFactory(corpus="corpus1", year=1910, text="one two three")
    }

    // 20 in 1920
    val d2 = for (_ <- (0 until 20).toList) yield {
      NovelFactory(corpus="corpus2", year=1920, text="four five six")
    }

    // 30 in 1930
    val d3 = for (_ <- (0 until 30).toList) yield {
      NovelFactory(corpus="corpus3", year=1930, text="seven eight nine")
    }

    val ds = spark.createDataset(d1 ++ d2 ++ d3)

    val rows = ExtBinCounts.mergeCounts(ds)

    forAll(Table(

      ("corpus", "year", "bin", "token", "pos", "count"),

      // 10 in 1910
      ("corpus1", 1910, 0,  "one",    "CD", 10),
      ("corpus1", 1910, 50, "two",    "CD", 10),
      ("corpus1", 1910, 99, "three",  "CD", 10),

      // 20 in 1920
      ("corpus2", 1920, 0,  "four",   "CD", 20),
      ("corpus2", 1920, 50, "five",   "CD", 20),
      ("corpus2", 1920, 99, "six",    "CD", 20),

      // 30 in 1930
      ("corpus3", 1930, 0,  "seven",  "CD", 30),
      ("corpus3", 1930, 50, "eight",  "CD", 30),
      ("corpus3", 1930, 99, "nine",   "CD", 30)

    )) { (
      corpus: String,
      year: Int,
      bin: Int,
      token: String,
      pos: String,
      count: Int
    ) =>

      val row = Ngram1Row(corpus, year, bin, token, pos, count)
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
      ("corpus", 1900, 0,   "one",    "CD", 1),
      ("corpus", 1900, 50,  "two",    "CD", 1),
      ("corpus", 1900, 99,  "three",  "CD", 1),

      // 1905 + 1906 -> 1910
      ("corpus", 1910, 0,   "one",    "CD", 2),
      ("corpus", 1910, 50,  "two",    "CD", 2),
      ("corpus", 1910, 99,  "three",  "CD", 2)

    )) { (
      corpus: String,
      year: Int,
      bin: Int,
      token: String,
      pos: String,
      count: Int
    ) =>

      val row = Ngram1Row(corpus, year, bin, token, pos, count)
      rows.filter(_ == row).count shouldEqual 1

    }

  }

}
