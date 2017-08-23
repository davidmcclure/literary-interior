

package lint.corpus

import lint.utils.Token


case class Unigram(
  corpus: String,
  year: Int,
  bin: Int,
  token: String,
  pos: String
)


case class NgramToken(
  token: String,
  pos: String
)


object NgramToken {

  def fromToken(token: Token): NgramToken = {
    NgramToken(token.token, token.pos)
  }

}


case class Ngram(
  binCount: Int,
  bin: Int,
  tokens: Seq[NgramToken]
)
