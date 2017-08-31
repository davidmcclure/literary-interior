

package lint.corpus


case class KWICMatch(
  corpus: String,
  identifier: String,
  title: String,
  authorFirst: String,
  authorLast: String,
  year: Int,
  token: String,
  pos: String,
  offset: Double,
  prefix: String,
  hit: String,
  suffix: String
)
