

package lint.chicago

import org.scalatest._
import org.scalatest.prop.TableDrivenPropertyChecks
import org.scalatest.prop.TableDrivenPropertyChecks._


class TextDirStripGutenbergParatextSpec extends FlatSpec with Matchers
  with TableDrivenPropertyChecks {

  // TODO: "End of Project Gutenberg's The Grandissimes"

  val headers = Table("header",
    "*** START OF THIS PROJECT GUTENBERG EBOOK ***",
    "***START OF THIS PROJECT GUTENBERG EBOOK***"
  )

  val footers = Table("footer",
    "*** END OF THIS PROJECT GUTENBERG EBOOK ***",
    "***END OF THIS PROJECT GUTENBERG EBOOK***"
  )

  "TextDir.stripGutenbergParatext" should
    "return the entire text, when no Gutenberg header / footer" in {

    val text = List(
      "line1",
      "line2",
      "line3"
    )

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
      )

      TextDir.stripGutenbergParatext(text) shouldEqual List(
        "line4",
        "line5",
        "line6"
      )

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
      )

      TextDir.stripGutenbergParatext(text) shouldEqual List(
        "line1",
        "line2",
        "line3"
      )

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
        )

        TextDir.stripGutenbergParatext(text) shouldEqual List(
          "line4",
          "line5",
          "line6"
        )

      }
    }

  }

}


class TextDirMkNovelSpec extends FreeSpec with Matchers {

  val path = getClass().getResource("/fixtures/chicago/CHICAGO_NOVEL_CORPUS").getFile
  val textDir = new TextDir(path)

  def getNovel(filename: String): Novel = {
    val source = NovelMetadataFactory(filename=filename)
    textDir.mkNovel(source)
  }

  "00000001" in {
    val novel = getNovel("00000001.txt")
    novel.text should include ("After talking of Herbert Spencer for an entire evening")
  }

  "00000003" in {
    val novel = getNovel("00000003.txt")
    novel.text should include ("The village lies in a trance like death.")
  }

  "00000013" - {

    val novel = getNovel("00000013.txt")

    "text" in {
      novel.text should include ("Olivia Ferrol leaned back in her chair, her hands folded upon her lap.")
    }

    "scrub header" in {
      novel.text.trim.startsWith("Produced by Al Haines") should be (true)
    }

    "scrub footer" in {
      novel.text.trim.endsWith("by Frances Hodgson Burnett") should be (true)
    }

  }

  "00000015" in {
    val novel = getNovel("00000015.txt")
    novel.text should include ("They paused a little within the obscurity of the corridor")
  }

  "00000021" in {
    val novel = getNovel("00000021.txt")
    novel.text should include ("THERE is Fred again with his arm around Jack Darcy's neck.")
  }

}
