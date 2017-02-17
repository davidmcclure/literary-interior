

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

  def getNovel(segment: String, identifier: String): Novel = {
    val url = getClass().getResource(s"/fixtures/gale/${segment}/Monographs/${identifier}.xml")
    Novel.fromPath(url.getFile)
  }

  "AMFCF0002-C00000-B0000400" - {

    val novel = getNovel("AMFCF0002-C00000", "AMFCF0002-C00000-B0000400")

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

    val novel = getNovel("AMFCF0002-C00000", "AMFCF0002-C00000-B0000600")

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

  "AMFCF0003-C00000-B0000100" - {

    val novel = getNovel("AMFCF0003-C00000", "AMFCF0003-C00000-B0000100")

    ".identifier" in {
      novel.identifier shouldEqual "AMFCF0003-C00000-B0000100"
    }

    ".title" in {
      novel.title shouldEqual "Brilla: By Anna M. Doling"
    }

    ".authorFirst" in {
      novel.authorFirst shouldEqual Some("Anna")
    }

    ".authorLast" in {
      novel.authorLast shouldEqual Some("Doling")
    }

    ".year" in {
      novel.year shouldEqual 1913
    }

    ".plainText" in {
      novel.plainText should include ("Captain Bawkah they call me.")
    }

  }

  "AMFCF0003-C00000-B0000200" - {

    val novel = getNovel("AMFCF0003-C00000", "AMFCF0003-C00000-B0000200")

    ".identifier" in {
      novel.identifier shouldEqual "AMFCF0003-C00000-B0000200"
    }

    ".title" in {
      novel.title shouldEqual "Virginia's Inheritance: By Cooke Don-Carlos"
    }

    ".authorFirst" in {
      novel.authorFirst shouldEqual Some("Cooke")
    }

    ".authorLast" in {
      novel.authorLast shouldEqual Some("Don-Carlos")
    }

    ".year" in {
      novel.year shouldEqual 1915
    }

    ".plainText" in {
      novel.plainText should include ("Ariminta Grannis knew it all the time")
    }

  }

  "AMFCF0002-C00000-B0169300 (no author)" - {

    val novel = getNovel("AMFCF0002-C00000", "AMFCF0002-C00000-B0169300")

    ".identifier" in {
      novel.identifier shouldEqual "AMFCF0002-C00000-B0169300"
    }

    ".title" in {
      novel.title shouldEqual "Tales of the Picket-Guard, or, the Blue Devils Driven from Camp: A Collection of Stories: Told by Three Rollicking Boys on Picket-Guard"
    }

    ".authorFirst" in {
      novel.authorFirst shouldEqual None
    }

    ".authorLast" in {
      novel.authorLast shouldEqual None
    }

    ".year" in {
      novel.year shouldEqual 1864
    }

    ".plainText" in {
      novel.plainText should include ("While our regiment was lying in winter quarters")
    }

  }

}
