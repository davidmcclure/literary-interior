

package lint.corpus

import lint.tokenizer._


final case class Text private (
  corpus: String,
  identifier: String,
  title: String,
  authorFirst: Option[String],
  authorLast: Option[String],
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
    authorFirst: Option[String],
    authorLast: Option[String],
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


trait Loader[T] {
  def listSources: List[T]
  def parse(source: T): Text
}
