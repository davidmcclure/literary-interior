

package lint.chicago

import java.io.File
import com.github.tototoshi.csv.CSVReader

import lint.config.Config


class NovelCSV(val path: String) {

  /* Map CSV rows into NovelMetadata instances.
   */
  def read: List[NovelMetadata] = {

    val reader = CSVReader.open(new File(path))

    for (row <- reader.allWithHeaders) yield NovelMetadata(
      bookId=row("BOOK_ID"),
      filename=row("FILENAME"),
      title=row("TITLE"),
      authLast=row("AUTH_LAST"),
      authFirst=row("AUTH_FIRST"),
      authId=row("AUTH_ID"),
      publCity=row("PUBL_CITY"),
      publisher=row("PUBLISHER"),
      publDate=row("PUBL_DATE").toInt,
      source=row("SOURCE"),
      nationality=row("NATIONALITY"),
      genre=row("GENRE")
    )

  }

}


object NovelCSV extends Config {

  /* Bind config novels CSV path.
   */
  def fromConfig: NovelCSV = {
    new NovelCSV(config.chicago.novelCSVPath)
  }

}
