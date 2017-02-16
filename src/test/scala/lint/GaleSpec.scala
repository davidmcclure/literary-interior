

package lint.gale

import org.scalatest._
import scala.xml.{XML,Elem,Node}
import scala.io.Source


class NovelSpec extends FreeSpec with Matchers {

  "Author" - {

    trait Novel {

      val xml = lint.xml.galeDefault(
        identifier="1",
        title="Moby Dick",
        authorFirst="Herman",
        authorLast="Melville",
        year=1851,
        tokens=Seq("Call", "me", "Ishmael.")
      )

      val novel = Novel.fromString(xml.toString.trim)

    }

    ".identifier" in new Novel {
      novel.identifier shouldEqual "1"
    }

    ".title" in new Novel {
      novel.title shouldEqual "Moby Dick"
    }

    ".authorFirst" in new Novel {
      novel.authorFirst shouldEqual "Herman"
    }

    ".authorLast" in new Novel {
      novel.authorLast shouldEqual "Melville"
    }

    ".year" in new Novel {
      novel.year shouldEqual 1851
    }

    ".plainText" in new Novel {
      novel.plainText shouldEqual "Call me Ishmael."
    }

  }

  "No author" - {

    trait Novel {

      val xml = lint.xml.galeNoAuthor(
        identifier="1",
        title="Moby Dick",
        year=1851,
        tokens=Seq("Call", "me", "Ishmael.")
      )

      val novel = Novel.fromString(xml.toString.trim)

    }

    ".identifier" in new Novel {
      novel.identifier shouldEqual "1"
    }

    ".title" in new Novel {
      novel.title shouldEqual "Moby Dick"
    }

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
