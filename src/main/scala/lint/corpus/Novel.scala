

package lint.corpus

import scala.math.floor
import scala.collection.mutable

import lint.utils.Token


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

  /* Accumulate Unigram -> count totals.
   */
  def unigramBinCounts(
    binCount: Int = 100,
    yearInterval: Int = 1
  ): Map[Unigram, Int] = {

    val counts = mutable.Map[Unigram, Int]().withDefaultValue(0)

    for (token <- tokens) {

      val roundedYear = Novel.roundYear(year, yearInterval)

      val bin = Novel.makeBin(token.offset, binCount)

      val key = Unigram(corpus, roundedYear, bin, token.token, token.pos)

      counts(key) += 1

    }

    counts.toMap

  }

  /* Accumulate Ngram -> count totals.
   */
  def ngramBinCounts(
    order: Int,
    binCount: Int = 10,
    minRank: Int = 10000
  ): Map[Ngram, Int] = {

    val counts = mutable.Map[Ngram, Int]().withDefaultValue(0)

    // Just take ngrams where all tokens are below a given rank.
    for (window <- tokens.sliding(order)) {

      val bin = Novel.makeBin(window(0).offset, binCount)

      val tokens = window.map(NgramToken.fromToken).toSeq

      val key = Ngram(binCount, bin, tokens)

      counts(key) += 1

    }

    counts.toMap

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
  def tokenOffsets(query: String): TokenOffsets = {

    val offsets = for (t <- tokens if t.token == query) yield t.offset

    TokenOffsets(
      corpus=corpus,
      identifier=identifier,
      title=title,
      authorFirst=authorFirst,
      authorLast=authorLast,
      year=year,
      offsets=offsets,
      tokenCount=tokens.length
    )

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

  /* Flatten an offset into a bin count, given a total number of bins.
   *
   * If the offset is 1 (last token), notch down into the bins-1 bin, to avoid
   * returning bins+1 bins.
   */
  def makeBin(offset: Double, binCount: Int) = {
    if (offset < 1) floor(offset * binCount).toInt
    else binCount - 1
  }

}
