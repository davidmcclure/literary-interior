

package lint.corpus

import org.scalatest._
import org.scalatest.prop.TableDrivenPropertyChecks
import org.scalatest.prop.TableDrivenPropertyChecks._

import lint.tokenizer.Tokenizer
import lint.corpus.NovelImplicits._


class NovelBinCountsSpec extends FlatSpec
  with Matchers with TableDrivenPropertyChecks {

  def getNovel(text: String = "text", year: Int = 2000): Novel = {

    val tokens = Tokenizer.tokenize(text)

    Novel(
      corpus="corpus",
      identifier="1",
      title="title",
      authorFirst="first",
      authorLast="last",
      year=year,
      text=text,
      tokens=tokens
    )

  }

  "Novel#binCounts" should "count tokens in each bin" in {

    // Two tokens in each bin.
    val novel = getNovel("one two three four five six seven eight")

    val counts = novel.binCounts(4)

    // TODO: Weird?
    val (c, y) = (novel.corpus, novel.year)

    counts(TokenBin(c, y, "one",    "CD", 0)) shouldEqual 1
    counts(TokenBin(c, y, "two",    "CD", 0)) shouldEqual 1

    counts(TokenBin(c, y, "three",  "CD", 1)) shouldEqual 1
    counts(TokenBin(c, y, "four",   "CD", 1)) shouldEqual 1

    counts(TokenBin(c, y, "five",   "CD", 2)) shouldEqual 1
    counts(TokenBin(c, y, "six",    "CD", 2)) shouldEqual 1

    counts(TokenBin(c, y, "seven",  "CD", 3)) shouldEqual 1
    counts(TokenBin(c, y, "eight",  "CD", 3)) shouldEqual 1

  }

  it should "accumulate token counts in each bin" in {

    // Two of each token in each bin.
    val novel = getNovel("one one two two three three four four")

    val counts = novel.binCounts(4)

    val (c, y) = (novel.corpus, novel.year)

    counts(TokenBin(c, y, "one",    "CD", 0)) shouldEqual 2
    counts(TokenBin(c, y, "two",    "CD", 1)) shouldEqual 2
    counts(TokenBin(c, y, "three",  "CD", 2)) shouldEqual 2
    counts(TokenBin(c, y, "four",   "CD", 3)) shouldEqual 2

  }

  it should "not round years by default" in {
    val novel = getNovel(year=1904)
    novel.binCounts().keys.head.year shouldEqual 1904
  }

  it should "round years when an interval is provided" in {

    val years = Table(
      ("year", "interval", "result"),
      (1904, 5, 1905),
      (1904, 10, 1900),
      (1905, 10, 1910)
    )

    forAll(years) { (year: Int, interval: Int, result: Int) =>

      val novel = getNovel(year=year)
      val counts = novel.binCounts(yearInterval=interval)

      counts.keys.head.year shouldEqual result

    }

  }

}
