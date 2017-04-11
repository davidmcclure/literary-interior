

package lint.chicago

import org.scalatest._
import org.scalatest.prop.TableDrivenPropertyChecks
import org.scalatest.prop.TableDrivenPropertyChecks._


class NovelCSVSpec extends FreeSpec with Matchers {

  val url = getClass().getResource("/fixtures/chicago/NOVELS_METADATA.csv")
  val reader = new NovelCSV(url.getFile)

  "CSV should parse without errors" in {
    val rows = reader.read
    rows.size should be > 0
  }

  // TODO: Spot-check rows.

}


class AuthorCSVSpec extends FreeSpec with Matchers {

  val url = getClass().getResource("/fixtures/chicago/AUTHORS_METADATA.csv")
  val reader = new AuthorCSV(url.getFile)

  "CSV should parse without errors" in {
    val rows = reader.read
    rows.size should be > 0
  }

  // TODO: Spot-check rows.

}


class TextDirStripGutenbergParatextSpec extends FlatSpec with Matchers
  with TableDrivenPropertyChecks {

  // TODO: Handle:
  // "End of Project Gutenberg's The Grandissimes"

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

    TextDir.stripGutenbergParatext(text) shouldEqual text.mkString("\n")

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
      )

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
        )

        TextDir.stripGutenbergParatext(text) shouldEqual List(
          "line4",
          "line5",
          "line6"
        ).mkString("\n")

      }
    }

  }

}


// TODO: Where to put this?
object NovelMetadataFactory {

  def apply(

    bookId: String = "1",
    filename: String = "1.txt",
    title: String = "title",
    authFirst: String = "first",
    authLast: String = "last",
    authId: String = "1",
    publCity: String = "city",
    publisher: String = "publisher",
    publDate: Int = 2000,
    source: String = "source",
    nationality: String = "nationality",
    genre: String = "genre"

  ) = NovelMetadata(

    bookId=bookId,
    filename=filename,
    title=title,
    authFirst=authFirst,
    authLast=authLast,
    authId=authId,
    publCity=publCity,
    publisher=publisher,
    publDate=publDate,
    source=source,
    nationality=nationality,
    genre=genre

  )

}


class TextDirMkNovelSpec extends FreeSpec with Matchers {

  val path = getClass().getResource("/fixtures/chicago/Texts").getFile
  val textDir = new TextDir(path)

  "00000001" in {
    val source = NovelMetadataFactory(filename="00000001.txt")
    val novel = textDir.mkNovel(source)
    novel.text should include ("After talking of Herbert Spencer for an entire evening")
  }

  "00000003" in {
    val source = NovelMetadataFactory(filename="00000003.txt")
    val novel = textDir.mkNovel(source)
    novel.text should include ("The village lies in a trance like death.")
  }

  "00000013" in {

    val source = NovelMetadataFactory(filename="00000013.txt")
    val novel = textDir.mkNovel(source)

    novel.text should include ("Olivia Ferrol leaned back in her chair, her hands folded upon her lap.")

    // Scrub header.
    novel.text should not include ("Character set encoding: ISO-8859-1")

    // Scrub footer.
    novel.text should not include ("This file should be named 35300-8.txt or 35300-8.zip")

  }

  "00000015" in {
    val source = NovelMetadataFactory(filename="00000015.txt")
    val novel = textDir.mkNovel(source)
    novel.text should include ("They paused a little within the obscurity of the corridor")
  }

  "00000021" in {
    val source = NovelMetadataFactory(filename="00000021.txt")
    val novel = textDir.mkNovel(source)
    novel.text should include ("THERE is Fred again with his arm around Jack Darcy's neck.")
  }

}
