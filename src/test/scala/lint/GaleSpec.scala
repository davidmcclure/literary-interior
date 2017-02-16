

package lint.gale

import org.scalatest._
import scala.xml.{XML,Elem,Node}
import scala.io.Source


class NovelSpec extends FreeSpec with Matchers {

  "Author" - {

    ".identifier" in {
      val novel = NovelSpec.makeNovel(identifier="1")
      novel.identifier shouldEqual "1"
    }

    ".title" in {
      val novel = NovelSpec.makeNovel(title="Moby Dick")
      novel.title shouldEqual "Moby Dick"
    }

    ".authorFirst" in {
      val novel = NovelSpec.makeNovel(authorFirst="Herman")
      novel.authorFirst shouldEqual "Herman"
    }

    ".authorLast" in {
      val novel = NovelSpec.makeNovel(authorLast="Melville")
      novel.authorLast shouldEqual "Melville"
    }

    ".year" in {
      val novel = NovelSpec.makeNovel(year=1851)
      novel.year shouldEqual 1851
    }

    ".plainText" in {
      val novel = NovelSpec.makeNovel(tokens=Seq("Call", "me", "Ishmael."))
      novel.plainText shouldEqual "Call me Ishmael."
    }

  }

  "No author" - {

    ".identifier" in {
      val xml = lint.xml.galeNoAuthor(identifier="1")
      val novel = Novel.fromString(xml.toString.trim)
      novel.identifier shouldEqual "1"
    }

    //".title" in {
      //val novel = NovelSpec.makeNovel(title="Moby Dick")
      //novel.title shouldEqual "Moby Dick"
    //}

    //".authorFirst" in {
      //val novel = NovelSpec.makeNovel(authorFirst="Herman")
      //novel.authorFirst shouldEqual "Herman"
    //}

    //".authorLast" in {
      //val novel = NovelSpec.makeNovel(authorLast="Melville")
      //novel.authorLast shouldEqual "Melville"
    //}

    //".year" in {
      //val novel = NovelSpec.makeNovel(year=1851)
      //novel.year shouldEqual 1851
    //}

    //".plainText" in {
      //val novel = NovelSpec.makeNovel(tokens=Seq("Call", "me", "Ishmael."))
      //novel.plainText shouldEqual "Call me Ishmael."
    //}

  }

}


object NovelSpec {

  def makeNovel(
    identifier: String = "1",
    title: String = "title",
    authorFirst: String = "first",
    authorLast: String = "last",
    year: Int = 1900,
    tokens: Seq[String] = Seq("token")
  ): Novel = {

    val xml = lint.xml.galeDefault(
      identifier = identifier,
      title = title,
      authorFirst = authorFirst,
      authorLast = authorLast,
      year = year,
      tokens = tokens
    )

    Novel.fromString(xml.toString.trim)

  }

}
