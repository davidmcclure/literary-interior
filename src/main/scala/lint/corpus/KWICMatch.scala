

package lint.corpus


case class KWICMatch(
  token: String,
  minOffset: Double,
  maxOffset: Double,
  corpus: String,
  identifier: String,
  title: String,
  authorFirst: String,
  authorLast: String,
  year: Int,
  offset: Double,
  snippet: String
)
