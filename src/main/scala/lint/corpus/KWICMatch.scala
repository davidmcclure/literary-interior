

package lint.corpus


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
