

package lint.gale

import java.io.File
import scala.xml.{XML,Elem,Node}
import scala.util.matching.Regex

import lint.corpus.{Text,Loader}
import lint.fileSystem.{FileSystem}
import lint.config.Config


class Novel(val xml: Elem) {

  def identifier: String = {
    (xml \\ "PSMID").head.text
  }

  def title: String = {
    (xml \\ "titleGroup" \ "fullTitle").head.text
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

  def year: Int = {
    val date = (xml \\ "pubDate" \ "pubDateStart").head.text
    date.slice(0, 4).toInt
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

  def mkText: Text = {
    Text(
      corpus="gale",
      identifier=identifier,
      title=title,
      authorFirst=authorFirst,
      authorLast=authorLast,
      year=year,
      text=plainText
    )
  }

}


object Novel {

  /* SAX parser, with DTD validation disabled.
   */
  def loader = {

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

  /* Make novel from a file.
   */
  def fromFile(file: File): Novel = {
    val tree = loader.loadFile(file)
    new Novel(tree)
  }

  /* Make novel from a file path.
   */
  def fromPath(path: String): Novel = {
    fromFile(new File(path))
  }

}


class Corpus(private val path: String) {

  val root = new File(path)

  /* Recursively list XML sources.
   */
  def listPaths = {
    FileSystem.walkTree(root).filter(_.toString.endsWith(".xml"))
  }

}


object Corpus extends Config {

  /* Read corpus root from config.
   */
  def fromConfig: Corpus = {
    new Corpus(config.gale.directory)
  }

}


object FileSystemLoader extends Loader[File] {

  /* List XML paths.
   */
  def listSources = {
    Corpus.fromConfig.listPaths.toList
  }

  /* XML -> Text.
   */
  def parse(source: File) = {
    Novel.fromFile(source).mkText
  }

}
