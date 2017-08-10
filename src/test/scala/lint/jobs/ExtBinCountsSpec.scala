

package lint.jobs

import org.scalatest._
import org.scalatest.prop.TableDrivenPropertyChecks
import org.scalatest.prop.TableDrivenPropertyChecks._

import lint.utils.Tokenize
import lint.corpus.NovelFactory
import lint.test.helpers.SparkTestSession


class ExtUnigramBinCountsMergeCountsSpec extends FlatSpec with Matchers
  with SparkTestSession with TableDrivenPropertyChecks {

  "ExtUnigramBinCounts.mergeCounts" should "index Unigram -> count" in {

    val spark = _spark
    import spark.implicits._

    // 10 in 1910
    val d1 = for (_ <- (0 until 10).toList) yield {
      NovelFactory(corpus="corpus1", year=1910, text="1 2 3")
    }

    // 20 in 1920
    val d2 = for (_ <- (0 until 20).toList) yield {
      NovelFactory(corpus="corpus2", year=1920, text="4 5 6")
    }

    // 30 in 1930
    val d3 = for (_ <- (0 until 30).toList) yield {
      NovelFactory(corpus="corpus3", year=1930, text="7 8 9")
    }

    val ds = spark.createDataset(d1 ++ d2 ++ d3)

    val rows = ExtUnigramBinCounts.mergeCounts(ds)

    forAll(Table(

      ("corpus", "year", "bin", "token", "pos", "count"),

      // 10 in 1910
      ("corpus1", 1910, 0,  "1", "CD", 10),
      ("corpus1", 1910, 50, "2", "CD", 10),
      ("corpus1", 1910, 99, "3", "CD", 10),

      // 20 in 1920
      ("corpus2", 1920, 0,  "4", "CD", 20),
      ("corpus2", 1920, 50, "5", "CD", 20),
      ("corpus2", 1920, 99, "6", "CD", 20),

      // 30 in 1930
      ("corpus3", 1930, 0,  "7", "CD", 30),
      ("corpus3", 1930, 50, "8", "CD", 30),
      ("corpus3", 1930, 99, "9", "CD", 30)

    )) { (
      corpus: String,
      year: Int,
      bin: Int,
      token: String,
      pos: String,
      count: Int
    ) =>

      val row = UnigramRow(corpus, year, bin, token, pos, count)
      rows.filter(_ == row).count shouldEqual 1

    }

  }

  it should "round years to the nearest decade" in {

    val spark = _spark
    import spark.implicits._

    val ds = spark.createDataset(Seq(
      NovelFactory(corpus="corpus", year=1904, text="1 2 3"),
      NovelFactory(corpus="corpus", year=1905, text="1 2 3"),
      NovelFactory(corpus="corpus", year=1906, text="1 2 3")
    ))

    val rows = ExtUnigramBinCounts.mergeCounts(ds)

    forAll(Table(

      ("corpus", "year", "token", "pos", "bin", "count"),

      // 1904 -> 1900
      ("corpus", 1900, 0,  "1", "CD", 1),
      ("corpus", 1900, 50, "2", "CD", 1),
      ("corpus", 1900, 99, "3", "CD", 1),

      // 1905 + 1906 -> 1910
      ("corpus", 1910, 0,  "1", "CD", 2),
      ("corpus", 1910, 50, "2", "CD", 2),
      ("corpus", 1910, 99, "3", "CD", 2)

    )) { (
      corpus: String,
      year: Int,
      bin: Int,
      token: String,
      pos: String,
      count: Int
    ) =>

      val row = UnigramRow(corpus, year, bin, token, pos, count)
      rows.filter(_ == row).count shouldEqual 1

    }

  }

}
