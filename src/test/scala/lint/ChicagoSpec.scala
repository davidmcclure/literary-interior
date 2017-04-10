

package lint.chicago

import org.scalatest._
import org.scalatest.prop.TableDrivenPropertyChecks
import org.scalatest.prop.TableDrivenPropertyChecks._


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


class TextDirStripGutenbergParatextSpec extends FlatSpec
  with Matchers with TableDrivenPropertyChecks {

  val headers = Table("header",
    "*** START OF THIS PROJECT GUTENBERG EBOOK ***",
    "***START OF THIS PROJECT GUTENBERG EBOOK***"
  )

  val footers = Table("footer",
    "*** END OF THIS PROJECT GUTENBERG EBOOK ***",
    "***END OF THIS PROJECT GUTENBERG EBOOK***"
  )

  "TextDir.stripGutenbergParatext()" should "return the entire text, when no Gutenberg header / footer" in {

    val text = List(
      "line1",
      "line2",
      "line3"
    ).mkString("\n")

    TextDir.stripGutenbergParatext(text) shouldEqual text

  }

  it should "strip out the header" in {

    forAll(headers) { header =>

      val text = List(
        "line1",
        "line2",
        "line3",
        header,
        "line4",
        "line5",
        "line6"
      ).mkString("\n")

      TextDir.stripGutenbergParatext(text) shouldEqual List(
        "line4",
        "line5",
        "line6"
      ).mkString("\n")

    }

  }

  it should "strip out the footer" in {

    forAll(footers) { footer =>

      val text = List(
        "line1",
        "line2",
        "line3",
        footer,
        "line4",
        "line5",
        "line6"
      ).mkString("\n")

      TextDir.stripGutenbergParatext(text) shouldEqual List(
        "line1",
        "line2",
        "line3"
      ).mkString("\n")

    }

  }

  it should "strip out the header + footer" in {

    forAll(headers) { header =>
      forAll(footers) { footer =>

        val text = List(
          "line1",
          "line2",
          "line3",
          header,
          "line4",
          "line5",
          "line6",
          footer,
          "line7",
          "line8",
          "line9"
        ).mkString("\n")

        TextDir.stripGutenbergParatext(text) shouldEqual List(
          "line4",
          "line5",
          "line6"
        ).mkString("\n")

      }
    }

  }

}
