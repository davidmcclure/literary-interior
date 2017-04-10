

package lint.chicago

import org.scalatest._


// TODO: Spot-check rows.
class NovelCSVSpec extends FreeSpec with Matchers {

  val url = getClass().getResource("/fixtures/chicago/NOVELS_METADATA.csv")
  val reader = new NovelCSV(url.getFile)

  "CSV should parse without errors" in {
    val rows = reader.read
    rows.size should be > 0
  }

}


class AuthorCSVSpec extends FreeSpec with Matchers {

  val url = getClass().getResource("/fixtures/chicago/AUTHORS_METADATA.csv")
  val reader = new AuthorCSV(url.getFile)

  "CSV should parse without errors" in {
    val rows = reader.read
    rows.size should be > 0
  }

}


class TextDirStripGutenbergParatextSpec extends FlatSpec with Matchers {

  "TextDir.stripGutenbergParatext()" should "return the entire text, when no Gutenberg header / footer" in {

    val text = List(
      "line1",
      "line2",
      "line3"
    ).mkString("\n")

    TextDir.stripGutenbergParatext(text) shouldEqual text

  }

  it should "strip out the header"

  it should "strip out the footer"

  it should "strip out the header + footer"

}
