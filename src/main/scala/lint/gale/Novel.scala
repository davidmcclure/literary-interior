

package lint.gale

import lint.Token


case class Novel(
  psmid: String,
  title: String,
  authorFirst: String,
  authorLast: String,
  language: String,
  year: Int,
  ocrPercentage: Double,
  documentType: String,
  text: String,
  tokens: Seq[Token]
)
