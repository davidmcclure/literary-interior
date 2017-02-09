

package lint.gale

import org.scalatest._
import scala.xml.{XML,Elem,Node}
import scala.io.Source
import com.hubspot.jinjava.Jinjava


class NovelSpec extends FlatSpec with Matchers {

  ".identifier()" should "provide the PSMID" in {
    val novel = NovelFixture(identifier="1")
    novel.identifier shouldEqual "1"
  }

  ".title()" should "provide the title" in {
    val novel = NovelFixture(title="Moby Dick")
    novel.title shouldEqual "Moby Dick"
  }

  ".authorFirst()" should "provide the author's first name" in {
    val novel = NovelFixture(authorFirst="Herman")
    novel.authorFirst shouldEqual "Herman"
  }

  ".authorLast()" should "provide the author's last name" in {
    val novel = NovelFixture(authorFirst="Melville")
    novel.authorFirst shouldEqual "Melville"
  }

  ".year()" should "provide the publication year" in {
    val novel = NovelFixture(year=1851)
    novel.year shouldEqual 1851
  }

}


object NovelFixture {

  def apply(
    identifier: String = "1",
    title: String = "Moby Dick",
    authorFirst: String = "Herman",
    authorLast: String = "Melville",
    year: Int = 1900
  ): Novel = {

    val stream = getClass.getResourceAsStream("/gale.xml")
    val template = Source.fromInputStream(stream).mkString

    val ctx = new java.util.HashMap[String, String]

    ctx.put("identifier", identifier)
    ctx.put("title", title)
    ctx.put("authorFirst", authorFirst)
    ctx.put("authorLast", authorLast)
    ctx.put("year", year.toString)

    val jinjava = new Jinjava
    val xml = jinjava.render(template, ctx)

    Novel.fromString(xml)

  }

}
