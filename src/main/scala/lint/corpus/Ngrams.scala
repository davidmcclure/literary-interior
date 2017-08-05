

package lint.corpus

import lint.utils.Token


case class Ngram1(
  corpus: String,
  year: Int,
  bin: Int,
  token: String,
  pos: String
)


case class Ngram2(
  corpus: String,
  year: Int,
  bin: Int,
  token1: String,
  pos1: String,
  token2: String,
  pos2: String
)
