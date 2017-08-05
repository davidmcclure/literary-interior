

package lint.corpus

import lint.utils.Tokenize


object NovelFactory {

  def apply(
    corpus: String = "corpus",
    identifier: String = "1",
    title: String = "title",
    authorFirst: String = "first",
    authorLast: String = "last",
    year: Int = 2000,
    text: String = "1 2 3"
  ): Novel = {

    val tokens = Tokenize(text)

    Novel(
      corpus=corpus,
      identifier=identifier,
      title=title,
      authorFirst=authorFirst,
      authorLast=authorLast,
      year=year,
      text=text,
      tokens=tokens
    )

  }

}
