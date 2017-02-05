

package lint.corpus

import java.io.FileInputStream
import scala.io.Source
import opennlp.tools.sentdetect._
import opennlp.tools.postag._
import opennlp.tools.tokenize._


final case class Token(
  token: String,
  start: Int,
  end: Int,
  offset: Double
)


case class Tokenizer(regex: String = "[a-z]+") {

  /* Given a string, generate a stream of Tokens.
   */
  def apply(text: String): Seq[Token] = {

    val matches = regex.r.findAllMatchIn(text.toLowerCase).toSeq

    val length = matches.length

    for ((m, i) <- matches.zipWithIndex) yield {
      new Token(m.matched, m.start, m.end, i.toDouble / length)
    }

  }

}


object Tokenizer {

  def loadSentenceModel = {
    val path = getClass.getResource("/en-sent.bin")
    val model = new SentenceModel(path)
    new SentenceDetectorME(model)
  }

  def loadTokenzerModel = {
    val path = getClass.getResource("/en-token.bin")
    val model = new TokenizerModel(path)
    new TokenizerME(model)
  }

  def loadPOSModel = {
    val path = getClass.getResource("/en-pos-maxent.bin")
    val model = new POSModel(path)
    new POSTaggerME(model)
  }

}


final case class Text private (
  identifier: String,
  title: String,
  authorFirst: String,
  authorLast: String,
  year: Int,
  text: String,
  tokens: Seq[Token]
)


object Text {

  /* Tokenize the raw text.
   */
  def apply(
    identifier: String,
    title: String,
    authorFirst: String,
    authorLast: String,
    year: Int,
    text: String
  ) = {

    val tokenize = new Tokenizer

    val tokens = tokenize(text)

    new Text(
      identifier,
      title,
      authorFirst,
      authorLast,
      year,
      text,
      tokens
    )

  }

}
