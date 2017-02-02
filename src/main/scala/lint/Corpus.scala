

package lint.corpus


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
