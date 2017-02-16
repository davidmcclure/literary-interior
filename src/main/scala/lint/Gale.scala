

package lint.gale

import java.io.File
import scala.xml.{XML,Elem,Node}
import scala.util.matching.Regex

import lint.text.Text


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

  /* Make novel from a file.
   */
  def fromFile(file: File): Novel = {
    val tree = loader.loadFile(file)
    new Novel(tree)
  }

}


// TODO: Different file.
object FileSystem {

  /* List a directory recursively.
   */
  def walkTree(f: File): Iterable[File] = {

    val children = new Iterable[File] {
      def iterator = {
        if (f.isDirectory) f.listFiles.iterator
        else Iterator.empty
      }
    }

    Seq(f) ++: children.flatMap(walkTree(_))

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


object Corpus {

  /* Read corpus root from config.
   * TODO
   */
  def fromConfig: Corpus = {
    new Corpus("/Users/dclure/Projects/data/stacks/gale")
  }

}


trait Loader[T] {
  def listSources: List[T]
  def parse(source: T): Text
}


object FileSystemLoader extends Loader[File] {

  def listSources = {
    Corpus.fromConfig.listPaths.toList
  }

  def parse(source: File) = {

    val novel = Novel.fromFile(source)

    Text(
      corpus="gale",
      identifier=novel.identifier,
      title=novel.title,
      authorFirst=novel.authorFirst,
      authorLast=novel.authorLast,
      year=novel.year,
      text=novel.plainText
    )

  }

}
