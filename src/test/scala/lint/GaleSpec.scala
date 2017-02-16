

package lint.gale

import org.scalatest._
import scala.xml.{XML,Elem,Node}
import scala.io.Source


class NovelSpec extends FlatSpec with Matchers {

  ".identifier" should "provide the PSMID" in {
    val novel = NovelSpec.makeNovel(identifier="1")
    novel.identifier shouldEqual "1"
  }

  ".title" should "provide the title" in {
    val novel = NovelSpec.makeNovel(title="Moby Dick")
    novel.title shouldEqual "Moby Dick"
  }

  ".authorFirst" should "provide the author's first name" in {
    val novel = NovelSpec.makeNovel(authorFirst="Herman")
    novel.authorFirst shouldEqual "Herman"
  }

  ".authorLast" should "provide the author's last name" in {
    val novel = NovelSpec.makeNovel(authorLast="Melville")
    novel.authorLast shouldEqual "Melville"
  }

  ".year" should "provide the publication year" in {
    val novel = NovelSpec.makeNovel(year=1851)
    novel.year shouldEqual 1851
  }

  ".plainText" should "provide joined tokens" in {
    val novel = NovelSpec.makeNovel(tokens=Seq("Call", "me", "Ishmael."))
    novel.plainText shouldEqual "Call me Ishmael."
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

    val xml = lint.xml.gale(
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
