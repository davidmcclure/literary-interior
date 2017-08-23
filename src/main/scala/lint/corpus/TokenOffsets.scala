

package lint.corpus


case class TokenOffsets(
  corpus: String,
  identifier: String,
  title: String,
  authorFirst: String,
  authorLast: String,
  year: Int,
  offsets: Seq[Double],
  tokenCount: Int
)
