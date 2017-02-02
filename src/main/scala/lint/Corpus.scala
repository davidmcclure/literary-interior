

package lint.corpus


case class Tokenizer(regex: String = "[a-z]+") {

  def apply(text: String): List[Token] = {

    val matches = regex.r.findAllMatchIn(text.toLowerCase).toList

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


final case class Text(
  identifier: String,
  title: String,
  authorFirst: String,
  authorLast: String,
  year: Int,
  text: String,
  tokens: List[Token]
)


object Text {

  def tokenize(
    identifier: String,
    title: String,
    authorFirst: String,
    authorLast: String,
    year: Int,
    text: String
  ): Text = {

    val tokenize = new Tokenizer

    val tokens = tokenize(text)

    Text(
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
