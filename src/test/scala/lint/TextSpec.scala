

package lint.text

import org.scalatest._
import lint.tokenizer._
import pprint._


class TextSpec extends FlatSpec with Matchers {

  "Text.apply()" should "tokenize the text" in {

    val text = Text(
      corpus="chicago",
      identifier="1",
      title="Moby Dick",
      authorFirst="Herman",
      authorLast="Melville",
      year=1851,
      text="Call me Ishmael."
    )

    text.tokens shouldEqual Tokenizer.tokenize("Call me Ishmael.")

  }

}
