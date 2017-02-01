

package lint.chicago

import java.io.File
import com.github.tototoshi.csv.CSVReader


case class Metadata(
  identifier: Int,
  title: String,
  authorFirst: String,
  authorLast: String,
  year: Int
)

class Corpus(val metadataPath: String, textPath: String) {

  // Read metadata CSV.
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

}

object Chicago extends App {

  val c = new Corpus(
    "/Users/dclure/Projects/data/stacks/Chicago Corpus/NOVELS_METADATA.csv",
    "/Users/dclure/Projects/data/stacks/Chicago Corpus/Texts"
  )

  println(c.metadata)

}
