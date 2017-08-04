

package lint.corpus

import org.scalatest._
import org.scalatest.prop.TableDrivenPropertyChecks
import org.scalatest.prop.TableDrivenPropertyChecks._

import lint.utils.Tokenize


class NovelBinCountsSpec extends FlatSpec with Matchers
  with TableDrivenPropertyChecks {

  "Novel#ngram1BinCounts" should "count tokens in each bin" in {

    // Two tokens in each bin.
    val novel = NovelFactory(text="one two three four five six seven eight")

    val counts = novel.ngram1BinCounts(4)

    forAll(Table(

      ("bin", "token", "pos", "count"),

      (0, "one",    "CD", 1),
      (0, "two",    "CD", 1),

      (1, "three",  "CD", 1),
      (1, "four",   "CD", 1),

      (2, "five",   "CD", 1),
      (2, "six",    "CD", 1),

      (3, "seven",  "CD", 1),
      (3, "eight",  "CD", 1)

    )) { (bin: Int, token: String, pos: String, count: Int) =>
      val key = Ngram1(novel.corpus, novel.year, bin, token, pos)
      counts(key) shouldEqual count
    }

  }

  it should "accumulate token counts in each bin" in {

    // Two of each token in each bin.
    val novel = NovelFactory(text="one one two two three three four four")

    val counts = novel.ngram1BinCounts(4)

    forAll(Table(

      ("bin", "token", "pos", "count"),

      (0, "one",    "CD", 2),
      (1, "two",    "CD", 2),
      (2, "three",  "CD", 2),
      (3, "four",   "CD", 2)

    )) { (bin: Int, token: String, pos: String, count: Int) =>
      val key = Ngram1(novel.corpus, novel.year, bin, token, pos)
      counts(key) shouldEqual count
    }

  }

  it should "not round years by default" in {
    val novel = NovelFactory(year=1904)
    novel.ngram1BinCounts().keys.head.year shouldEqual 1904
  }

  it should "round years when an interval is provided" in {

    forAll(Table(

      ("year", "interval", "result"),
      (1904, 5,  1905),
      (1904, 10, 1900),
      (1905, 10, 1910)

    )) { (year: Int, interval: Int, result: Int) =>

      val novel = NovelFactory(year=year)
      val counts = novel.ngram1BinCounts(yearInterval=interval)

      counts.keys.head.year shouldEqual result

    }

  }

}


class NovelTokenOffsetsSpec extends FlatSpec with Matchers {

  "Novel#tokenOffsets" should "pluck out offsets for token" in {
    val row = NovelFactory(text="a b a b a").tokenOffsets("a")
    row.offsets shouldEqual Seq(0, 0.5, 1)
  }

  "Novel#tokenOffsets" should "provide token count" in {
    val row = NovelFactory(text="a b a b a").tokenOffsets("a")
    row.tokenCount shouldEqual 5
  }

}
