

package literaryinterior.corpus

import lindex.corpora.literaryinterior.{Novel => RawNovel}
import lindex.tokenizer.Token


case class TokenMatch(
  corpus: String,
  identifier: String,
  title: String,
  authorFirst: Option[String],
  authorLast: Option[String],
  year: Int,
  offset: Double,
  snippet: String
)


//case class TokenPosPercentile(
  //token: String,
  //pos: String,
  //percentile: Int
//)


object implicits {

  implicit class EnrichedNovel(val novel: RawNovel) {

    /* Probe for KWIC matches.
     */
    def kwic(
      query: String,
      minOffset: Double,
      maxOffset: Double,
      radius: Int
    ): Seq[TokenMatch] = {

      // Find matching tokens, inside offset range.
      for (
        token <- novel.tokens
        if (token.token == query)
        if (token.offset >= minOffset)
        if (token.offset <= maxOffset)
      ) yield {

        // Get snippet / match character offsets.
        val c1 = token.start - radius
        val c2 = token.start
        val c3 = token.end
        val c4 = token.end + radius

        val prefix = novel.text.slice(c1, c2)
        val hit = novel.text.slice(c2, c3)
        val suffix = novel.text.slice(c3, c4)

        val snippet = prefix + s"***${hit}***" + suffix

        TokenMatch(
          corpus=novel.corpus,
          identifier=novel.identifier,
          title=novel.title,
          authorFirst=novel.authorFirst,
          authorLast=novel.authorLast,
          year=novel.year,
          offset=token.offset,
          snippet=snippet
        )

      }

    }

  }

}
