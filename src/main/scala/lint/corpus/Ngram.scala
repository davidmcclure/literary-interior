

package lint.corpus


case class Ngram(
  binCount: Int,
  bin: Int,
  tokens: Seq[NgramToken]
)
