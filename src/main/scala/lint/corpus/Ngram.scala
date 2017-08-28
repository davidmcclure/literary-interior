

package lint.corpus

import scala.io.Source


case class Ngram(
  binCount: Int,
  bin: Int,
  tokens: Seq[NgramToken]
) {

  def allFrequent: Boolean = {
    tokens.forall(x => Ngram.tokens10k.contains(x.token))
  }

}


object Ngram {

  val tokens10k: Set[String] = {
    val stream = getClass.getResourceAsStream("/tokens10k.txt")
    Source.fromInputStream(stream).getLines.toSet
  }

}
