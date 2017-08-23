

package lint.corpus

import org.scalatest._
import org.scalatest.prop.TableDrivenPropertyChecks
import org.scalatest.prop.TableDrivenPropertyChecks._

import lint.utils.Tokenize


class NovelUnigramBinCountsSpec extends FlatSpec with Matchers
  with TableDrivenPropertyChecks {

  "Novel#unigramBinCounts" should "count tokens in each bin" in {

    // Two tokens in each bin.
    val novel = NovelFactory(text="1 2 3 4 5 6 7 8")

    val counts = novel.unigramBinCounts(4)

    forAll(Table(

      ("bin", "token", "count"),

      (0, "1", 1),
      (0, "2", 1),

      (1, "3", 1),
      (1, "4", 1),

      (2, "5", 1),
      (2, "6", 1),

      (3, "7", 1),
      (3, "8", 1)

    )) { (bin: Int, token: String, count: Int) =>
      val key = Unigram(novel.corpus, novel.year, bin, token, "CD")
      counts(key) shouldEqual count
    }

  }

  it should "accumulate counts in each bin" in {

    // Two of each token in each bin.
    val novel = NovelFactory(text="1 1 2 2 3 3 4 4")

    val counts = novel.unigramBinCounts(4)

    forAll(Table(

      ("bin", "token", "count"),

      (0, "1", 2),
      (1, "2", 2),
      (2, "3", 2),
      (3, "4", 2)

    )) { (bin: Int, token: String, count: Int) =>
      val key = Unigram(novel.corpus, novel.year, bin, token, "CD")
      counts(key) shouldEqual count
    }

  }

  it should "not round years by default" in {
    val novel = NovelFactory(year=1904)
    novel.unigramBinCounts().keys.head.year shouldEqual 1904
  }

  it should "round years when an interval is provided" in {

    forAll(Table(

      ("year", "interval", "result"),
      (1904, 5,  1905),
      (1904, 10, 1900),
      (1905, 10, 1910)

    )) { (year: Int, interval: Int, result: Int) =>

      val novel = NovelFactory(year=year)
      val counts = novel.unigramBinCounts(yearInterval=interval)

      counts.keys.head.year shouldEqual result

    }

  }

}


class NovelNgramBinCountsSpec extends FlatSpec with Matchers
  with TableDrivenPropertyChecks {

  "Novel#ngramBinCounts" should "count 1-grams" in {

    val novel = NovelFactory(text="""
      1 1
      2 2
      3 3
      4 4
    """)

    val counts = novel.ngramBinCounts(1, 4)

    forAll(Table(

      ("bin", "token", "count"),

      (0, "1", 2),
      (1, "2", 2),
      (2, "3", 2),
      (3, "4", 2)

    )) { (bin: Int, token: String, count: Int) =>

      val tokens = Seq(NgramToken(token, "CD"))

      val key = Ngram(4, bin, tokens)

      counts(key) shouldEqual count

    }

  }

  it should "count 2-grams" in {

    val novel = NovelFactory(text="""
      1 1 1
      2 2 2
      3 3 3
      4 4 4
    """)

    val counts = novel.ngramBinCounts(2, 4)

    forAll(Table(

      ("bin", "token1", "token2", "count"),

      (0, "1", "1", 2),
      (0, "1", "2", 1),

      (1, "2", "2", 2),
      (1, "2", "3", 1),

      (2, "3", "3", 2),
      (2, "3", "4", 1),

      (3, "4", "4", 2)

    )) { (bin: Int, token1: String, token2: String, count: Int) =>

      val tokens = Seq(
        NgramToken(token1, "CD"),
        NgramToken(token2, "CD")
      )

      val key = Ngram(4, bin, tokens)

      counts(key) shouldEqual count

    }

  }

  it should "count 3-grams" in {

    val novel = NovelFactory(text="""
      1 1 1 1
      2 2 2 2
      3 3 3 3
      4 4 4 4
    """)

    val counts = novel.ngramBinCounts(3, 4)

    forAll(Table(

      ("bin", "token1", "token2", "token3", "count"),

      (0, "1", "1", "1", 2),
      (0, "1", "1", "2", 1),

      (1, "2", "2", "2", 2),
      (1, "2", "2", "3", 1),

      (2, "3", "3", "3", 2),
      (2, "3", "3", "4", 1),

      (3, "4", "4", "4", 2)

    )) { (
      bin: Int,
      token1: String,
      token2: String,
      token3: String,
      count: Int
    ) =>

      val tokens = Seq(
        NgramToken(token1, "CD"),
        NgramToken(token2, "CD"),
        NgramToken(token3, "CD")
      )

      val key = Ngram(4, bin, tokens)

      counts(key) shouldEqual count

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
