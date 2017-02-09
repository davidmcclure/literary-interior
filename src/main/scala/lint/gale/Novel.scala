

package lint.gale

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

  // Singleton SAX parser, with DTD validation disabled.
  val loader = {

    val factory = javax.xml.parsers.SAXParserFactory.newInstance()

    factory.setFeature(
      "http://apache.org/xml/features/nonvalidating/load-external-dtd",
      false
    )

    XML.withSAXParser(factory.newSAXParser)

  }

  /* Make novel from XML string.
   */
  def fromString(markup: String): Novel = {
    val tree = loader.loadString(markup)
    new Novel(tree)
  }

  /* Make novel from a file path.
   */
  def fromPath(path: String): Novel = {
    val tree = loader.loadFile(path)
    new Novel(tree)
  }

}
