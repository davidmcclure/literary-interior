

package lint.corpora.literaryinterior

import lint.tokenizer.Token


case class Novel(
  corpus: String,
  identifier: String,
  title: String,
  authorFirst: Option[String],
  authorLast: Option[String],
  year: Int,
  text: String,
  tokens: Seq[Token]
)


object Novel {

  /* Map Gale novel.
   */
  def fromGaleNovel(novel: lint.corpora.gale.Novel) = Novel(
    corpus="gale",
    identifier=novel.psmid,
    title=novel.title,
    authorFirst=novel.authorFirst,
    authorLast=novel.authorLast,
    year=novel.year,
    text=novel.text,
    tokens=novel.tokens
  )

  /* Map Chicago novel.
   */
  def fromChicagoNovel(novel: lint.corpora.chicago.Novel) = Novel(
    corpus="chicago",
    identifier=novel.bookId,
    title=novel.title,
    authorFirst=Some(novel.authFirst),
    authorLast=Some(novel.authLast),
    year=novel.publDate,
    text=novel.text,
    tokens=novel.tokens
  )

}
