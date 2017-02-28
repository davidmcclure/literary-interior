

package lint.gale

import java.io.File
import scala.xml.{XML,Elem,Node}
import scala.util.matching.Regex

import lint.tokenizer.{Tokenizer,Token}
import lint.corpus.Text
import lint.fileSystem.FileSystem
import lint.config.Config


case class Novel(
  psmid: String,
  title: String,
  authorFirst: Option[String],
  authorLast: Option[String],
  language: String,
  year: Int,
  ocrPercentage: Double,
  documentType: String,
  text: String,
  tokens: Seq[Token]
) extends Text


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

    Novel(
      psmid=psmid,
      title=title,
      authorFirst=authorFirst,
      authorLast=authorLast,
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

    val factory = javax.xml.parsers.SAXParserFactory.newInstance()

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
    new Corpus(config.gale.corpusDir)
  }

}


object Loader {

  /* List XML paths.
   */
  def sources: List[File] = {
    Corpus.fromConfig.listPaths.toList
  }

  /* XML -> Text.
   */
  def parse(source: File): Novel = {
    NovelXML.fromFile(source).mkNovel
  }

}
