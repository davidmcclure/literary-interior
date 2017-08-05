

package lint.corpus

import org.scalatest._
import org.scalatest.prop.TableDrivenPropertyChecks
import org.scalatest.prop.TableDrivenPropertyChecks._

import lint.utils.Tokenize


class NovelNgram1BinCountsSpec extends FlatSpec with Matchers
  with TableDrivenPropertyChecks {

  "Novel#ngram1BinCounts" should "count tokens in each bin" in {

    // Two tokens in each bin.
    val novel = NovelFactory(text="1 2 3 4 5 6 7 8")

    val counts = novel.ngram1BinCounts(4)

    forAll(Table(

      ("bin", "token", "pos", "count"),

      (0, "1", "CD", 1),
      (0, "2", "CD", 1),

      (1, "3", "CD", 1),
      (1, "4", "CD", 1),

      (2, "5", "CD", 1),
      (2, "6", "CD", 1),

      (3, "7", "CD", 1),
      (3, "8", "CD", 1)

    )) { (bin: Int, token: String, pos: String, count: Int) =>
      val key = Ngram1(novel.corpus, novel.year, bin, token, pos)
      counts(key) shouldEqual count
    }

  }

  it should "accumulate counts in each bin" in {

    // Two of each token in each bin.
    val novel = NovelFactory(text="1 1 2 2 3 3 4 4")

    val counts = novel.ngram1BinCounts(4)

    forAll(Table(

      ("bin", "token", "pos", "count"),

      (0, "1", "CD", 2),
      (1, "2", "CD", 2),
      (2, "3", "CD", 2),
      (3, "4", "CD", 2)

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


class NovelNgram2BinCountsSpec extends FlatSpec with Matchers
  with TableDrivenPropertyChecks {

  "Novel#ngram2BinCounts" should "count tokens in each bin" in {

    // Two tokens in each bin.
    val novel = NovelFactory(text="1 2 3 4 5 6 7 8")

    val counts = novel.ngram2BinCounts(4)

    forAll(Table(

      ("bin", "token1", "pos1", "token2", "pos2", "count"),

      (0, "1", "CD", "2", "CD", 1),
      (1, "3", "CD", "4", "CD", 1),
      (2, "5", "CD", "6", "CD", 1),
      (3, "7", "CD", "8", "CD", 1)

    )) { (
      bin: Int,
      token1: String,
      pos1: String,
      token2: String,
      pos2: String,
      count: Int
    ) =>

      val key = Ngram2(
        novel.corpus, novel.year, bin,
        token1, pos1, token2, pos2
      )

      counts(key) shouldEqual count

    }

  }

  it should "accumulate counts in each bin" in {

    // 2x 2-grams in each bin.
    val novel = NovelFactory(text="1 1 1 2 2 2 3 3 3 4 4 4")

    val counts = novel.ngram2BinCounts(4)

    forAll(Table(

      ("bin", "token1", "pos1", "token2", "pos2", "count"),

      (0, "1", "CD", "1", "CD", 2),
      (0, "1", "CD", "2", "CD", 1),

      (1, "2", "CD", "2", "CD", 2),
      (1, "2", "CD", "3", "CD", 1),

      (2, "3", "CD", "3", "CD", 2),
      (2, "3", "CD", "4", "CD", 1),

      (3, "4", "CD", "4", "CD", 2)

    )) { (
      bin: Int,
      token1: String,
      pos1: String,
      token2: String,
      pos2: String,
      count: Int
    ) =>

      val key = Ngram2(
        novel.corpus, novel.year, bin,
        token1, pos1, token2, pos2
      )

      counts(key) shouldEqual count

    }

  }

  it should "not round years by default" in {
    val novel = NovelFactory(year=1904)
    novel.ngram2BinCounts().keys.head.year shouldEqual 1904
  }

  it should "round years when an interval is provided" in {

    forAll(Table(

      ("year", "interval", "result"),
      (1904, 5,  1905),
      (1904, 10, 1900),
      (1905, 10, 1910)

    )) { (year: Int, interval: Int, result: Int) =>

      val novel = NovelFactory(year=year)
      val counts = novel.ngram2BinCounts(yearInterval=interval)

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
