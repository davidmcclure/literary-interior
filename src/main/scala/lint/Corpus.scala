

package lint.corpus

import lint.tokenizer.Token


case class TextData(
  text: String,
  tokens: Seq[Token]
)


trait Text {

  val text: String
  val tokens: Seq[Token]

  def normalize: TextData = {
    TextData(text, tokens)
  }

}


trait Loader[T] {
  def listSources: List[T]
  def parse(source: T): Text
}


//final case class Text private (
  //corpus: String,
  //identifier: String,
  //title: String,
  //authorFirst: Option[String],
  //authorLast: Option[String],
  //year: Int,
  //text: String,
  //tokens: Seq[Token]
//)


//object Text {

  /* Tokenize the raw text.
   */
  //def apply(
    //corpus: String,
    //identifier: String,
    //title: String,
    //authorFirst: Option[String],
    //authorLast: Option[String],
    //year: Int,
    //text: String
  //) = {

    //val tokens = Tokenizer.tokenize(text)

    //new Text(
      //corpus,
      //identifier,
      //title,
      //authorFirst,
      //authorLast,
      //year,
      //text,
      //tokens
    //)

  //}

//}





//object Text {

  /* Tokenize the raw text.
   */
  //def apply(corpus: String, identifier: String, text: String) = {
    //val tokens = Tokenizer.tokenize(text)
    //new Text(corpus, identifier, text, tokens)
  //}

//}
