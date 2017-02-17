

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
      novel.authorFirst shouldEqual Some("Herman")
    }

    ".authorLast" in new Novel {
      novel.authorLast shouldEqual Some("Melville")
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

    ".authorFirst" in new Novel {
      novel.authorFirst shouldEqual None
    }

    ".authorLast" in new Novel {
      novel.authorLast shouldEqual None
    }

    ".year" in new Novel {
      novel.year shouldEqual 1851
    }

    ".plainText" in new Novel {
      novel.plainText shouldEqual "Call me Ishmael."
    }

  }

}


class NovelFixturesSpec extends FreeSpec with Matchers {

  "AMFCF0002-C00000-B0000400" - {

    val url = getClass().getResource("/fixtures/gale/AMFCF0002-C00000/Monographs/AMFCF0002-C00000-B0000400.xml")
    val novel = Novel.fromPath(url.getFile)

    ".identifier" in {
      novel.identifier shouldEqual "AMFCF0002-C00000-B0000400"
    }

    ".title" in {
      novel.title shouldEqual "Illustrated Lives and Adventures of the Desperadoes of the New World: Containing an Account of the Different Modes of Lynching, the Cane Hill Murders, the Victims, the Execution, the Justicifation, Etc., Etc: As Well as the Lives of the Principal Duellist"
    }

    ".authorFirst" in {
      novel.authorFirst shouldEqual Some("Alfred")
    }

    ".authorLast" in {
      novel.authorLast shouldEqual Some("Arrington")
    }

    ".year" in {
      novel.year shouldEqual 1849
    }

    ".plainText" - {

      "titlePage" in {
        novel.plainText should not include ("THE LIVES MODERATOR BY CHARLES SOTM")
      }

      "frontmatter" in {
        novel.plainText should not include ("The scenes presented in the following pages")
      }

      "bodyPage" in {
        novel.plainText should include ("The court of the lynchers has been migratory.")
      }

      "backmatter" in {
        novel.plainText should not include ("T. B. PETERSON, No. 98")
      }

    }

  }

  "AMFCF0002-C00000-B0000600" - {

    val url = getClass().getResource("/fixtures/gale/AMFCF0002-C00000/Monographs/AMFCF0002-C00000-B0000600.xml")
    val novel = Novel.fromPath(url.getFile)

    ".identifier" in {
      novel.identifier shouldEqual "AMFCF0002-C00000-B0000600"
    }

    ".title" in {
      novel.title shouldEqual "Agnes, or, the Possessed: A Revelation of Mesmerism: By T. S. Arthur"
    }

    ".authorFirst" in {
      novel.authorFirst shouldEqual Some("Timothy")
    }

    ".authorLast" in {
      novel.authorLast shouldEqual Some("Arthur")
    }

    ".year" in {
      novel.year shouldEqual 1848
    }

    ".plainText" in {
      novel.plainText should include ("We are fearfully and wonderfully made!")
    }

  }

}
