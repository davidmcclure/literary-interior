

package lindex.corpora.literaryinterior

import lindex.tokenizer.Token


trait NovelSchema {
  val corpus: String
  val identifier: String
  val title: String
  val authorFirst: Option[String]
  val authorLast: Option[String]
  val year: Int
  val text: String
  val tokens: Seq[Token]
}


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


object Novel {

  /* Map Gale novel.
   */
  def fromGaleNovel(novel: lindex.corpora.gale.Novel) = Novel(
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
  def fromChicagoNovel(novel: lindex.corpora.chicago.Novel) = Novel(
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
