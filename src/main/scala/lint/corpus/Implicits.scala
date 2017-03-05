

package lint.corpus

import scala.collection.mutable.Map
import scala.math.floor


case class TokenBin(token: String, pos: String, bin: Int)


case class KWICMatch(
  corpus: String,
  identifier: String,
  title: String,
  authorFirst: String,
  authorLast: String,
  year: Int,
  offset: Double,
  snippet: String
)


object implicits {

  implicit class RichNovel(n: Novel) {

    /* Count the number of times that each (token, POS) pair appears in each
     * percentile of the text.
     */
    def binCounts(bins: Int = 100): Map[TokenBin, Int] = {

      val counts = Map[TokenBin, Int]().withDefaultValue(0)

      for (token <- n.tokens) {

        // If offset is 1 (last token), notch down into the bins-1 bin, to
        // avoid returning bins+1 bins.
        val bin =
          if (token.offset < 1) floor(token.offset * bins).toInt
          else bins - 1

        val tpp = TokenBin(token.token, token.pos, bin)

        counts(tpp) += 1

      }

      counts

    }

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
        token <- n.tokens
        if (token.token == query)
        if (token.offset >= minOffset)
        if (token.offset <= maxOffset)
      ) yield {

        // Get snippet / match character offsets.
        val c1 = token.start - radius
        val c2 = token.start
        val c3 = token.end
        val c4 = token.end + radius

        // Slice out segments.
        val prefix = n.text.slice(c1, c2)
        val hit = n.text.slice(c2, c3)
        val suffix = n.text.slice(c3, c4)

        // Format the snippet.
        val snippet = prefix + s"***${hit}***" + suffix

        KWICMatch(
          corpus=n.corpus,
          identifier=n.identifier,
          title=n.title,
          authorFirst=n.authorFirst,
          authorLast=n.authorLast,
          year=n.year,
          offset=token.offset,
          snippet=snippet
        )

      }

    }

  }

}
