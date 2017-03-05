

package lint.corpus

import org.scalatest._

import lint.tokenizer.Tokenizer
import lint.corpus.implicits._


class NovelBinCountsSpec extends FlatSpec with Matchers {

  def getNovel(text: String): Novel = {

    val tokens = Tokenizer.tokenize(text)

    Novel(
      corpus="corpus",
      identifier="1",
      title="title",
      authorFirst="first",
      authorLast="last",
      year=2000,
      text=text,
      tokens=tokens
    )

  }

  "Novel#binCounts" should "count tokens in each bin" in {

    val novel = getNovel("one two three four five six seven eight")

    val counts = novel.binCounts(4)

    counts(TokenBin("one",   "CD", 0)) shouldEqual 1
    counts(TokenBin("two",   "CD", 0)) shouldEqual 1

    counts(TokenBin("three", "CD", 1)) shouldEqual 1
    counts(TokenBin("four",  "CD", 1)) shouldEqual 1

    counts(TokenBin("five",  "CD", 2)) shouldEqual 1
    counts(TokenBin("six",   "CD", 2)) shouldEqual 1

    counts(TokenBin("seven", "CD", 3)) shouldEqual 1
    counts(TokenBin("eight", "CD", 3)) shouldEqual 1

  }

  it should "accumulate token counts in each bin" in {

    // Two of each token in each bin.
    val novel = getNovel("one one two two three three four four")

    val counts = novel.binCounts(4)

    counts(TokenBin("one",   "CD", 0)) shouldEqual 2
    counts(TokenBin("two",   "CD", 1)) shouldEqual 2
    counts(TokenBin("three", "CD", 2)) shouldEqual 2
    counts(TokenBin("four",  "CD", 3)) shouldEqual 2

  }

}
