

package lindex.corpus

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
)


object Novel {

  /* Map Gale novel.
   */
  def fromGaleNovel(novel: lindex.gale.Novel) = Novel(
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
  def fromChicagoNovel(novel: lindex.chicago.Novel) = Novel(
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
