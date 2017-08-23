

package lint.corpus

import lint.utils.Token


case class NgramToken(
  token: String,
  pos: String
)


object NgramToken {

  def fromToken(token: Token): NgramToken = {
    NgramToken(token.token, token.pos)
  }

}
