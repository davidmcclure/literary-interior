

package lint.corpus

import lint.tokenizer.Token


case class KWICMatch(
  corpus: String,
  identifier: String,
  title: String,
  authorFirst: Option[String],
  authorLast: Option[String],
  year: Int,
  offset: Double,
  snippet: String
)


case class Novel(
  corpus: String,
  identifier: String,
  title: String,
  authorFirst: Option[String],
  authorLast: Option[String],
  year: Int,
  text: String,
  tokens: Seq[Token]
) {

  /* Given a query token, find all occurrences within an offset range and
   * provide match instances.
   */
  def kwic(
    query: String,
    minOffset: Double,
    maxOffset: Double,
    radius: Int
  ): Seq[KWICMatch] = {

    for (
      token <- tokens
      if (token.token == query)
      if (token.offset >= minOffset)
      if (token.offset <= maxOffset)
    ) yield {

      val c1 = token.start - radius
      val c2 = token.start
      val c3 = token.end
      val c4 = token.end + radius

      val prefix = text.slice(c1, c2)
      val hit = text.slice(c2, c3)
      val suffix = text.slice(c3, c4)

      val snippet = prefix + s"***${hit}***" + suffix

      KWICMatch(
        corpus=corpus,
        identifier=identifier,
        title=title,
        authorFirst=authorFirst,
        authorLast=authorLast,
        year=year,
        offset=token.offset,
        snippet=snippet
      )

    }

  }

}


object Novel {

  /* Map Gale novel.
   */
  def fromGaleNovel(novel: lint.gale.Novel) = Novel(
    corpus="gale",
    identifier=novel.psmid,
    title=novel.title,
    authorFirst=novel.authorFirst,
    authorLast=novel.authorLast,
    year=novel.year,
    text=novel.text,
    tokens=novel.tokens
  )

  /* Map Chicago novel.
   */
  def fromChicagoNovel(novel: lint.chicago.Novel) = Novel(
    corpus="chicago",
    identifier=novel.bookId,
    title=novel.title,
    authorFirst=Some(novel.authFirst),
    authorLast=Some(novel.authLast),
    year=novel.publDate,
    text=novel.text,
    tokens=novel.tokens
  )

}
