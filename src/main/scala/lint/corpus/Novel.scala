

package lint.corpus

import scala.math.floor
import scala.collection.mutable.Map

import lint.utils.Token


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


case class Novel(
  corpus: String,
  identifier: String,
  title: String,
  authorFirst: String,
  authorLast: String,
  year: Int,
  text: String,
  tokens: Seq[Token]
) {

  /* Count the number of times that each (token, POS) pair appears in each
   * percentile of the text.
   */
  def binCounts(
    bins: Int = 100,
    yearInterval: Int = 1
  ): Map[TokenBin, Int] = {

    val counts = Map[TokenBin, Int]().withDefaultValue(0)

    for (token <- tokens) {

      val roundedYear = Novel.roundYear(year, yearInterval)

      // If offset is 1 (last token), notch down into the bins-1 bin, to
      // avoid returning bins+1 bins.
      val bin =
        if (token.offset < 1) floor(token.offset * bins).toInt
        else bins - 1

      val key = TokenBin(corpus, roundedYear, token.token, token.pos, bin)

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

      // Slice out segments.
      val prefix = text.slice(c1, c2)
      val hit = text.slice(c2, c3)
      val suffix = text.slice(c3, c4)

      // Format the snippet.
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

  /* Pluck out offsets for a query token.
   */
  def tokenOffsets(query: String): Seq[Double] = {
    for (token <- tokens if token.token == query) yield token.offset
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
    authorFirst=novel.authFirst,
    authorLast=novel.authLast,
    year=novel.publDate,
    text=novel.text,
    tokens=novel.tokens
  )

  /* Round a year to the nearest N years.
   */
  def roundYear(year: Int, interval: Int = 10) = {
    (Math.round(year.toDouble / interval) * interval).toInt
  }

}
