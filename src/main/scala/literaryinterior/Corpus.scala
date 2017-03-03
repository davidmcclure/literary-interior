

package literaryinterior.corpus

import lindex.corpora.literaryinterior.NovelSchema
import lindex.tokenizer.Token


case class Novel(
  corpus: String,
  identifier: String,
  title: String,
  authorFirst: Option[String],
  authorLast: Option[String],
  year: Int,
  text: String,
  tokens: Seq[Token]
) extends NovelSchema
