

package lint.tokenizer

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

  val sentenceModel = {
    val path = getClass.getResource("/en-sent.bin")
    new SentenceModel(path)
  }

  val tokenizerModel = {
    val path = getClass.getResource("/en-token.bin")
    new TokenizerModel(path)
  }

  val posModel = {
    val path = getClass.getResource("/en-pos-maxent.bin")
    new POSModel(path)
  }

  /* Convert a string into a stream of Tokens.
   */
  def tokenize(text: String): Seq[Token] = {

    val sentenceDetector = new SentenceDetectorME(sentenceModel)
    val tokenizer = new TokenizerME(tokenizerModel)
    val posTagger = new POSTaggerME(posModel)

    // Get sentence boundaries.
    val sentPos = sentenceDetector.sentPosDetect(text)

    val tokens = sentPos.flatMap(sentSpan => {

      // Extract sentence text.
      val sentence = text.slice(sentSpan.getStart, sentSpan.getEnd)

      // Get token boundaries.
      val tokenPos = tokenizer.tokenizePos(sentence)

      // Extract tokens
      val tokens = for (tokenSpan <- tokenPos) yield {
        sentence.slice(tokenSpan.getStart, tokenSpan.getEnd)
      }

      // POS-tag tokens.
      val tags = posTagger.tag(tokens)

      // Zip together (token, POS, start, end).
      for (
         (token, tag, span) <-
         (tokens, tags, tokenPos).zipped.toList
      ) yield {

        val start = sentSpan.getStart + span.getStart
        val end = sentSpan.getStart + span.getEnd

        (token.toLowerCase, tag, start, end)

      }

    })

    val length = tokens.length

    // Thread in the 0-1 offset.
    for (((token, tag, start, end), i) <- tokens.zipWithIndex) yield {
      new Token(token, tag, start, end, i.toDouble / (length-1))
    }

  }

}


object Test extends App {

  val t1 = System.nanoTime

  for (_ <- 0 to 1000) {
    Tokenizer.tokenize("My name is David. Does this work???")
  }

  val t2 = System.nanoTime
  println(t2-t1)

}
