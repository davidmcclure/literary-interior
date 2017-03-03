

package literaryinterior.corpus

import lindex.corpora.literaryinterior.NovelSchema
import lindex.tokenizer.Token


case class Novel(
  corpus: String,
  identifier: String,
  title: String,
  authorFirst: Option[String],
  authorLast: Option[String],
  year: Int,
  text: String,
  tokens: Seq[Token]
) extends NovelSchema {

  /* Probe for KWIC matches.
   */
  def kwic(
    query: String,
    minOffset: Double,
    maxOffset: Double,
    radius: Int
  ): Seq[KWICMatch] = {

    // Find matching tokens, inside offset range.
    for (
      token <- tokens
      if (token.token == query)
      if (token.offset >= minOffset)
      if (token.offset <= maxOffset)
    ) yield {

      // Get snippet / match character offsets.
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
