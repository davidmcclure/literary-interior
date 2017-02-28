

package lint.text

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
