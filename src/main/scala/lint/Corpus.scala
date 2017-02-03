

package lint.corpus

import java.io.FileInputStream
import scala.io.Source
import opennlp.tools.sentdetect._
import pprint.pprintln


case class Tokenizer(regex: String = "[a-z]+") {

  // Sentence detector.
  val sentPath = getClass.getResource("/en-sent.bin")
  val sentModel = new SentenceModel(sentPath)
  val sentDetector = new SentenceDetectorME(sentModel)

  /* Given a string, generate a stream of Tokens.
   */
  def apply(text: String): Seq[Token] = {

    pprintln(sentDetector.sentDetect(text))

    val matches = regex.r.findAllMatchIn(text.toLowerCase).toSeq

    val length = matches.length

    for ((m, i) <- matches.zipWithIndex) yield {
      new Token(m.matched, m.start, m.end, i.toDouble / length)
    }

  }

}


final case class Token(
  token: String,
  start: Int,
  end: Int,
  offset: Double
)


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


object Corpus extends App {
  val tokenize = new Tokenizer
  tokenize("This is a sentence. And another one.")
}
