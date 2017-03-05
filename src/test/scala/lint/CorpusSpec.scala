

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

    counts(TokenPosBin("one",   "CD", 0)) shouldEqual 1
    counts(TokenPosBin("two",   "CD", 0)) shouldEqual 1

    counts(TokenPosBin("three", "CD", 1)) shouldEqual 1
    counts(TokenPosBin("four",  "CD", 1)) shouldEqual 1

    counts(TokenPosBin("five",  "CD", 2)) shouldEqual 1
    counts(TokenPosBin("six",   "CD", 2)) shouldEqual 1

    counts(TokenPosBin("seven", "CD", 3)) shouldEqual 1
    counts(TokenPosBin("eight", "CD", 3)) shouldEqual 1

  }

  it should "accumulate token counts in each bin" in {

    // Two of each token in each bin.
    val novel = getNovel("one one two two three three four four")

    val counts = novel.binCounts(4)

    counts(TokenPosBin("one",   "CD", 0)) shouldEqual 2
    counts(TokenPosBin("two",   "CD", 1)) shouldEqual 2
    counts(TokenPosBin("three", "CD", 2)) shouldEqual 2
    counts(TokenPosBin("four",  "CD", 3)) shouldEqual 2

  }

}
