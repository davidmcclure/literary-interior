

package lint.gale

import java.io.File
import javax.xml.parsers.SAXParserFactory
import scala.xml.{XML,Elem,Node}

import lint.tokenizer.{Tokenizer,Token}


class NovelXML(val xml: Elem) {

  def psmid: String = {
    (xml \\ "PSMID").head.text
  }

  def title: String = {
    (xml \\ "fullTitle").head.text
  }

  def author: Option[Node] = {

    val authors = xml \\ "author"

    // Take the first author with a <first> child.
    if (authors.length == 0) None else {
      Some(authors.filter(a => (a \ "first").length == 1).head)
    }

  }

  def authorFirst: Option[String] = {
    author match {
      case Some(a) => Some((a \ "first").head.text)
      case None => None
    }
  }

  def authorLast: Option[String] = {
    author match {
      case Some(a) => Some((a \ "last").head.text)
      case None => None
    }
  }

  def language: String = {
    (xml \\ "language").head.text
  }

  def year: Int = {
    val date = (xml \\ "pubDate" \ "pubDateStart").head.text
    date.slice(0, 4).toInt
  }

  def ocrPercentage: Double = {
    (xml \\ "ocr").head.text.toDouble
  }

  def documentType: String = {
    (xml \\ "documentType").head.text
  }

  def plainText: String = {

    (xml \\ "page")

      // Take words on "body" pages.
      .filter(p => (p \ "@type").text == "bodyPage")
      .flatMap(_ \\ "wd")

      // Get text, join on space.
      .map(_.text)
      .mkString(" ")

  }

  /* Map XML into Novel.
   */
  def mkNovel: Novel = {

    val text = plainText
    val tokens = Tokenizer.tokenize(text)

    // TODO: Pass forward the options?
    Novel(
      psmid=psmid,
      title=title,
      authorFirst=authorFirst.getOrElse(null),
      authorLast=authorLast.getOrElse(null),
      language=language,
      year=year,
      ocrPercentage=ocrPercentage,
      documentType=documentType,
      text=text,
      tokens=tokens
    )

  }

}


object NovelXML {

  /* SAX parser, with DTD validation disabled.
   */
  def loader = {

    val factory = SAXParserFactory.newInstance()

    factory.setFeature(
      "http://apache.org/xml/features/nonvalidating/load-external-dtd",
      false
    )

    XML.withSAXParser(factory.newSAXParser)

  }

  /* Make novel from XML string.
   */
  def fromString(markup: String): NovelXML = {
    val tree = loader.loadString(markup)
    new NovelXML(tree)
  }

  /* Make novel from a file.
   */
  def fromFile(file: File): NovelXML = {
    val tree = loader.loadFile(file)
    new NovelXML(tree)
  }

  /* Make novel from a file path.
   */
  def fromPath(path: String): NovelXML = {
    fromFile(new File(path))
  }

}
