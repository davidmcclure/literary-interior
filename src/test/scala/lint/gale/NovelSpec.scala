

package lint.gale

import org.scalatest._
import scala.xml.{XML,Elem,Node}
import scala.io.Source
import com.hubspot.jinjava.Jinjava


class NovelSpec extends FlatSpec with Matchers {

  ".identifier()" should "provide the PSMID" in {
    val xml = lint.xml.gale(identifier="1")
    val novel = Novel.fromString(xml.toString.trim)
    novel.identifier shouldEqual "1"
  }

  ".title()" should "provide the title" in {
    val xml = lint.xml.gale(title="Moby Dick")
    val novel = Novel.fromString(xml.toString.trim)
    novel.title shouldEqual "Moby Dick"
  }

  ".authorFirst()" should "provide the author's first name" in {
    val xml = lint.xml.gale(authorFirst="Herman")
    val novel = Novel.fromString(xml.toString.trim)
    novel.authorFirst shouldEqual "Herman"
  }

  ".authorLast()" should "provide the author's last name" in {
    val xml = lint.xml.gale(authorLast="Melville")
    val novel = Novel.fromString(xml.toString.trim)
    novel.authorLast shouldEqual "Melville"
  }

  ".year()" should "provide the publication year" in {
    val xml = lint.xml.gale(year=1851)
    val novel = Novel.fromString(xml.toString.trim)
    novel.year shouldEqual 1851
  }

}
