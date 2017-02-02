

package lint.chicago

import scala.io.Source
import java.io.File
import org.apache.commons.io.FilenameUtils
import com.github.tototoshi.csv.CSVReader


case class Metadata(
  identifier: Int,
  title: String,
  authorFirst: String,
  authorLast: String,
  year: Int
)

abstract class Corpus {
  val metadata: Map[Int, Metadata]
  def plainText(identifier: Int): String
}

class LocalCorpus(
  val metadataPath: String,
  textPath: String
) extends Corpus {

  private val reader = CSVReader.open(new File(metadataPath))

  // Get (id, metadata) tuples.
  private val pairs = for (row <- reader.allWithHeaders) yield {

    val md = new Metadata(
      identifier=row("BOOK_ID").toInt,
      title=row("TITLE"),
      authorFirst=row("AUTH_FIRST"),
      authorLast=row("AUTH_LAST"),
      year=row("PUBL_DATE").toInt
    )

    (md.identifier, md)

  }

  // Map id -> metadata.
  val metadata: Map[Int, Metadata] = pairs.toMap

  /* Read plain text by ID.
   */
  def plainText(identifier: Int): String = {

    // Left-pad zeros to 8 digits.
    val basename = "%08d".format(identifier)

    val path = FilenameUtils.concat(textPath, s"${basename}.txt")
    Source.fromFile(path).getLines.mkString

  }

}

object Chicago extends App {

  val c = new LocalCorpus(
    "/Users/dclure/Projects/data/stacks/Chicago Corpus/NOVELS_METADATA.csv",
    "/Users/dclure/Projects/data/stacks/Chicago Corpus/Texts"
  )

  println(c.plainText(1))

}
