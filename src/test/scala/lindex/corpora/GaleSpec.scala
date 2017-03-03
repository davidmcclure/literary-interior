

package lindex.corpora.gale

import org.scalatest._
import scala.xml.{XML,Elem,Node}
import scala.io.Source


class NovelXMLSpec extends FreeSpec with Matchers {

  def getNovel(segment: String, psmid: String): NovelXML = {
    val url = getClass().getResource(s"/fixtures/gale/${segment}/Monographs/${psmid}.xml")
    NovelXML.fromPath(url.getFile)
  }

  "AMFCF0002-C00000-B0000400" - {

    val novel = getNovel("AMFCF0002-C00000", "AMFCF0002-C00000-B0000400")

    ".psmid" in {
      novel.psmid shouldEqual "AMFCF0002-C00000-B0000400"
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

    ".language" in {
      novel.language shouldEqual "English"
    }

    ".year" in {
      novel.year shouldEqual 1849
    }

    ".ocrPercentage" in {
      novel.ocrPercentage shouldEqual 56.66
    }

    ".documentType" in {
      novel.documentType shouldEqual "Monograph"
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

    ".psmid" in {
      novel.psmid shouldEqual "AMFCF0002-C00000-B0000600"
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

    ".language" in {
      novel.language shouldEqual "English"
    }

    ".year" in {
      novel.year shouldEqual 1848
    }

    ".ocrPercentage" in {
      novel.ocrPercentage shouldEqual 63.70
    }

    ".documentType" in {
      novel.documentType shouldEqual "Monograph"
    }

    ".plainText" in {
      novel.plainText should include ("We are fearfully and wonderfully made!")
    }

  }

  "AMFCF0003-C00000-B0000100" - {

    val novel = getNovel("AMFCF0003-C00000", "AMFCF0003-C00000-B0000100")

    ".psmid" in {
      novel.psmid shouldEqual "AMFCF0003-C00000-B0000100"
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

    ".language" in {
      novel.language shouldEqual "English"
    }

    ".year" in {
      novel.year shouldEqual 1913
    }

    ".ocrPercentage" in {
      novel.ocrPercentage shouldEqual 65.10
    }

    ".documentType" in {
      novel.documentType shouldEqual "Monograph"
    }

    ".plainText" in {
      novel.plainText should include ("Captain Bawkah they call me.")
    }

  }

  "AMFCF0003-C00000-B0000200" - {

    val novel = getNovel("AMFCF0003-C00000", "AMFCF0003-C00000-B0000200")

    ".psmid" in {
      novel.psmid shouldEqual "AMFCF0003-C00000-B0000200"
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

    ".language" in {
      novel.language shouldEqual "English"
    }

    ".year" in {
      novel.year shouldEqual 1915
    }

    ".ocrPercentage" in {
      novel.ocrPercentage shouldEqual 65.99
    }

    ".documentType" in {
      novel.documentType shouldEqual "Monograph"
    }

    ".plainText" in {
      novel.plainText should include ("Ariminta Grannis knew it all the time")
    }

  }

  "AMFCF0002-C00000-B0169300 (no author)" - {

    val novel = getNovel("AMFCF0002-C00000", "AMFCF0002-C00000-B0169300")

    ".psmid" in {
      novel.psmid shouldEqual "AMFCF0002-C00000-B0169300"
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

    ".language" in {
      novel.language shouldEqual "English"
    }

    ".year" in {
      novel.year shouldEqual 1864
    }

    ".ocrPercentage" in {
      novel.ocrPercentage shouldEqual 50.70
    }

    ".documentType" in {
      novel.documentType shouldEqual "Monograph"
    }

    ".plainText" in {
      novel.plainText should include ("While our regiment was lying in winter quarters")
    }

  }

  "AMFCF0002-C00000-B1020300 (multiple authors)" - {

    val novel = getNovel("AMFCF0002-C00000", "AMFCF0002-C00000-B1020300")

    ".psmid" in {
      novel.psmid shouldEqual "AMFCF0002-C00000-B1020300"
    }

    ".title" in {
      novel.title shouldEqual "The Elixir of Life, or, Robert's Pilgrimage: An Allegory: By Eleve …"
    }

    ".authorFirst" in {
      novel.authorFirst shouldEqual Some("H.")
    }

    ".authorLast" in {
      novel.authorLast shouldEqual Some("Stowe")
    }

    ".language" in {
      novel.language shouldEqual "English"
    }

    ".year" in {
      novel.year shouldEqual 1890
    }

    ".ocrPercentage" in {
      novel.ocrPercentage shouldEqual 60.88
    }

    ".documentType" in {
      novel.documentType shouldEqual "Monograph"
    }

    ".plainText" in {
      novel.plainText should include ("A vast land filled with wild and uncultivated people")
    }

  }

}
