

package lint.gail

import java.io.File
import scala.xml.{XML,Elem,Node}


class Novel(val xml: Elem) {

  def identifier: String = {
    (xml \\ "PSMID").head.text
  }

  def title: String = {
    (xml \\ "titleGroup" \ "fullTitle").head.text
  }

  def author: Node = {
    (xml \\ "author").head
  }

  def authorFirst: String = {
    (author \ "first").head.text
  }

  def authorLast: String = {
    (author \ "last").head.text
  }

  def year: Int = {
    val date = (xml \\ "pubDate" \ "pubDateStart").head.text
    date.slice(0, 4).toInt
  }

  def plainText: String = {
    val words = xml \\ "page" \\ "wd"
    val texts = for (w <- words) yield w.text
    texts.mkString(" ")
  }

}

object Novel {

  /* Read Gail XML, disabling DTD validation.
   */
  def fromFile(path: String): Novel = {

    val factory = javax.xml.parsers.SAXParserFactory.newInstance()

    factory.setFeature(
      "http://apache.org/xml/features/nonvalidating/load-external-dtd",
      false
    )

    val tree = XML.withSAXParser(factory.newSAXParser).loadFile(path)

    new Novel(tree)

  }

}

object Lint extends App {
  val novel = Novel.fromFile("/Users/dclure/Projects/data/stacks/gail/AMFCF0002-C00000-B1001700.xml")
  println(novel.plainText)
}
