

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

    val words = for {
      page <- xml \\ "page"
      if (page \ "@type").text == "bodyPage"
      word <- page \\ "wd"
    } yield word

    val texts = for (w <- words) yield w.text

    texts.mkString(" ")

  }

}


object Novel {

  // Singleton SAX parser.
  val factory = {

    val saxFactory = javax.xml.parsers.SAXParserFactory.newInstance()

    saxFactory.setFeature(
      "http://apache.org/xml/features/nonvalidating/load-external-dtd",
      false
    )

    saxFactory

  }

  /* Read Gail XML, disabling DTD validation.
   */
  def fromFile(path: String): Novel = {
    val tree = XML.withSAXParser(factory.newSAXParser).loadFile(path)
    new Novel(tree)
  }

}
