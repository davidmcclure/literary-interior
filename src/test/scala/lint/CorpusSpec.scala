

package lint.corpus

import org.scalatest._
import org.scalatest.prop.TableDrivenPropertyChecks
import org.scalatest.prop.TableDrivenPropertyChecks._

import lint.tokenizer.Tokenize
import lint.corpus.NovelImplicits._


object NovelFactory {

  def apply(
    corpus: String = "corpus",
    identifier: String = "1",
    title: String = "title",
    authorFirst: String = "first",
    authorLast: String = "last",
    year: Int = 2000,
    text: String = "text"
  ): Novel = {

    val tokens = Tokenize(text)

    Novel(
      corpus=corpus,
      identifier=identifier,
      title=title,
      authorFirst=authorFirst,
      authorLast=authorLast,
      year=year,
      text=text,
      tokens=tokens
    )

  }

}


class NovelBinCountsSpec extends FlatSpec with Matchers
  with TableDrivenPropertyChecks {

  "Novel#binCounts" should "count tokens in each bin" in {

    // Two tokens in each bin.
    val novel = NovelFactory(text="one two three four five six seven eight")

    val counts = novel.binCounts(4)

    forAll(Table(

      ("token", "pos", "bin", "count"),

      ("one",   "CD", 0, 1),
      ("two",   "CD", 0, 1),

      ("three", "CD", 1, 1),
      ("four",  "CD", 1, 1),

      ("five",  "CD", 2, 1),
      ("six",   "CD", 2, 1),

      ("seven", "CD", 3, 1),
      ("eight", "CD", 3, 1)

    )) { (token: String, pos: String, bin: Int, count: Int) =>
      val key = TokenBin(novel.corpus, novel.year, token, pos, bin)
      counts(key) shouldEqual count
    }

  }

  it should "accumulate token counts in each bin" in {

    // Two of each token in each bin.
    val novel = NovelFactory(text="one one two two three three four four")

    val counts = novel.binCounts(4)

    forAll(Table(

      ("token", "pos", "bin", "count"),
      ("one",   "CD", 0, 2),
      ("two",   "CD", 1, 2),
      ("three", "CD", 2, 2),
      ("four",  "CD", 3, 2)

    )) { (token: String, pos: String, bin: Int, count: Int) =>
      val key = TokenBin(novel.corpus, novel.year, token, pos, bin)
      counts(key) shouldEqual count
    }

  }

  it should "not round years by default" in {
    val novel = NovelFactory(year=1904)
    novel.binCounts().keys.head.year shouldEqual 1904
  }

  it should "round years when an interval is provided" in {

    forAll(Table(

      ("year", "interval", "result"),
      (1904, 5, 1905),
      (1904, 10, 1900),
      (1905, 10, 1910)

    )) { (year: Int, interval: Int, result: Int) =>

      val novel = NovelFactory(year=year)
      val counts = novel.binCounts(yearInterval=interval)

      counts.keys.head.year shouldEqual result

    }

  }

}
