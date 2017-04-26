

package lint.corpus

import scala.collection.mutable.Map
import scala.math.floor


case class TokenBin(
  corpus: String,
  year: Int,
  token: String,
  pos: String,
  bin: Int
)


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


object NovelImplicits {

  implicit class RichNovel(n: Novel) {

    /* Count the number of times that each (token, POS) pair appears in each
     * percentile of the text.
     */
    def binCounts(
      bins: Int = 100,
      yearInterval: Int = 1
    ): Map[TokenBin, Int] = {

      val counts = Map[TokenBin, Int]().withDefaultValue(0)

      for (token <- n.tokens) {

        val year = RichNovel.roundYear(n.year, yearInterval)

        // If offset is 1 (last token), notch down into the bins-1 bin, to
        // avoid returning bins+1 bins.
        val bin =
          if (token.offset < 1) floor(token.offset * bins).toInt
          else bins - 1

        val key = TokenBin(n.corpus, year, token.token, token.pos, bin)

        counts(key) += 1

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

    /* Pluck out offsets for a query token.
     */
    def tokenOffsets(query: String): Seq[Double] = {
      for (token <- n.tokens if token.token == query) yield token.offset
    }

  }

  implicit object RichNovel {

    /* Round a year to the nearest N years.
     */
    def roundYear(year: Int, interval: Int = 10) = {
      (Math.round(year.toDouble / interval) * interval).toInt
    }

  }

}
