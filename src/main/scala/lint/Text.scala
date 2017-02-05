

package lint.text

import lint.tokenizer._


final case class Text private (
  corpus: String,
  identifier: String,
  title: String,
  authorFirst: String,
  authorLast: String,
  year: Int,
  text: String,
  tokens: Seq[Token]
)


object Text {

  /* Tokenize the raw text.
   */
  def apply(
    corpus: String,
    identifier: String,
    title: String,
    authorFirst: String,
    authorLast: String,
    year: Int,
    text: String
  ) = {

    val tokens = Tokenizer.tokenize(text)

    new Text(
      corpus,
      identifier,
      title,
      authorFirst,
      authorLast,
      year,
      text,
      tokens
    )

  }

}
