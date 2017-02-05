

package lint.corpus

import java.io.FileInputStream
import scala.io.Source
import opennlp.tools.sentdetect._
import opennlp.tools.postag._
import opennlp.tools.tokenize._
import pprint._


final case class Token(
  token: String,
  pos: String,
  start: Int,
  end: Int,
  offset: Double
)


object Tokenizer {

  val sentenceModel = loadSentenceModel
  val tokenizerModel = loadTokenizerModel
  val posModel = loadPOSModel

  def loadSentenceModel = {
    val path = getClass.getResource("/en-sent.bin")
    val model = new SentenceModel(path)
    new SentenceDetectorME(model)
  }

  def loadTokenizerModel = {
    val path = getClass.getResource("/en-token.bin")
    val model = new TokenizerModel(path)
    new TokenizerME(model)
  }

  def loadPOSModel = {
    val path = getClass.getResource("/en-pos-maxent.bin")
    val model = new POSModel(path)
    new POSTaggerME(model)
  }

  /* Convert a string into a stream of Tokens.
   */
  def tokenize(text: String): Seq[Token] = {

    // Get sentence boundaries.
    val sentPos = sentenceModel.sentPosDetect(text)

    val tokens = sentPos.flatMap(sentSpan => {

      // Extract sentence text.
      val sentence = text.slice(sentSpan.getStart, sentSpan.getEnd)

      // Get token boundaries.
      val tokenPos = tokenizerModel.tokenizePos(sentence)

      // Extract tokens
      val tokens = for (tokenSpan <- tokenPos) yield {
        sentence.slice(tokenSpan.getStart, tokenSpan.getEnd)
      }

      // POS-tag tokens.
      val tags = posModel.tag(tokens)

      // Zip together (token, POS, start, end).
      for (
         (token, tag, span) <-
         (tokens, tags, tokenPos).zipped.toList
      ) yield {

        val start = sentSpan.getStart + span.getStart
        val end = sentSpan.getStart + span.getEnd

        (token, tag, start, end)

      }

    })

    val length = tokens.length

    // Thread in the 0-1 offset.
    for (((token, tag, start, end), i) <- tokens.zipWithIndex) yield {
      new Token(token, tag, start, end, i.toDouble / (length-1))
    }

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

    val tokens = Tokenizer.tokenize(text)

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
  val tokens = Tokenizer.tokenize("My name is David. I love Kara.")
  pprintln(tokens)
}
