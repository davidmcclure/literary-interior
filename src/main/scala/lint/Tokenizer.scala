

package lint.tokenizer

import java.io.FileInputStream
import scala.io.Source
import opennlp.tools.sentdetect._
import opennlp.tools.postag._
import opennlp.tools.tokenize._


case class Token(
  token: String,
  pos: String,
  start: Int,
  end: Int,
  offset: Double
)


object Tokenizer {

  // Sentences

  val sentenceModel = {
    val path = getClass.getResource("/models/en-sent.bin")
    new SentenceModel(path)
  }

  def getSentPos(text: String) = {
    val detector = new SentenceDetectorME(sentenceModel)
    detector.sentPosDetect(text)
  }

  // Tokens

  val tokenizerModel = {
    val path = getClass.getResource("/models/en-token.bin")
    new TokenizerModel(path)
  }

  def getTokenPos(sentence: String) = {
    val tokenizer = new TokenizerME(tokenizerModel)
    tokenizer.tokenizePos(sentence)
  }

  // POS-tags

  val posModel = {
    val path = getClass.getResource("/models/en-pos-maxent.bin")
    new POSModel(path)
  }

  def getPosTags(tokens: Array[String]) = {
    val tagger = new POSTaggerME(posModel)
    tagger.tag(tokens)
  }

  /* Convert a string into a stream of Tokens.
   */
  def tokenize(text: String): Seq[Token] = {

    // Get sentence boundaries.
    val sentPos = getSentPos(text)

    val tokens = sentPos.flatMap(sentSpan => {

      // Extract sentence text.
      val sentence = text.slice(sentSpan.getStart, sentSpan.getEnd)

      // Get token boundaries.
      val tokenPos = getTokenPos(sentence)

      // Extract tokens
      val tokens = for (tokenSpan <- tokenPos) yield {
        sentence.slice(tokenSpan.getStart, tokenSpan.getEnd)
      }

      // POS-tag tokens.
      val tags = getPosTags(tokens)

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
