

package lint.corpus


case class Tokenizer(regex: String = "[a-z]+") {

  def apply(text: String): Seq[Token] = {

    val matches = regex.r.findAllMatchIn(text.toLowerCase).toSeq

    val length = matches.length

    for ((m, i) <- matches.zipWithIndex) yield {
      new Token(m.matched, m.start, m.end, i.toDouble / length)
    }

  }

}


final case class Token(
  token: String,
  start: Int,
  end: Int,
  offset: Double
)


final case class Text private (
  identifier: String,
  title: String,
  authorFirst: String,
  authorLast: String,
  year: Int,
  text: String,
  tokens: Seq[Token]
)


object Text {

  def apply(
    identifier: String,
    title: String,
    authorFirst: String,
    authorLast: String,
    year: Int,
    text: String
  ) = {

    val tokenize = new Tokenizer

    val tokens = tokenize(text)

    new Text(
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
