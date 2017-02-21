

package lint.chicago

import java.io.File
import java.nio.file.Paths
import scala.io.Source
import com.github.tototoshi.csv.CSVReader
import lint.config.Config
import lint.corpus.{Text,Loader}


case class NovelMetadata(
  bookId: String,
  filename: String,
  title: String,
  authLast: String,
  authFirst: String,
  publDate: Int
)


class FileSystemNovelsCSV(val path: String) {

  /* Map CSV rows into NovelMetadata instances.
   */
  def read: List[NovelMetadata] = {

    val reader = CSVReader.open(new File(path))

    for (row <- reader.allWithHeaders) yield {
      NovelMetadata(
        bookId=row("BOOK_ID"),
        filename=row("FILENAME"),
        title=row("TITLE"),
        authLast=row("AUTH_LAST"),
        authFirst=row("AUTH_FIRST"),
        publDate=row("PUBL_DATE").toInt
      )
    }

  }

}


object FileSystemNovelsCSV extends Config {

  /* Bind config novels CSV path.
   */
  def fromConfig: FileSystemNovelsCSV = {
    new FileSystemNovelsCSV(config.chicago.novelMetadataPath)
  }

}


class FileSystemTextDir(val path: String) {

  /* Given a book ID, hydrate the text.
   */
  def read(bookId: String): String = {
    val textPath = Paths.get(path, s"${bookId}.txt").toString
    Source.fromFile(textPath).getLines.mkString
  }

  /* Given a metadata row, build a text.
   */
  def mkText(row: NovelMetadata): Text = {
    Text(
      corpus="chicago",
      identifier=row.bookId,
      title=row.title,
      authorFirst=Some(row.authFirst),
      authorLast=Some(row.authLast),
      year=row.publDate,
      text=read(row.bookId)
    )
  }

}


object FileSystemTextDir extends Config {

  /* Bind config text path.
   */
  def fromConfig: FileSystemTextDir = {
    new FileSystemTextDir(config.chicago.textDirectory)
  }

}


object FileSystemLoader extends Loader[NovelMetadata] {

  /* List novel metadata rows.
   */
  def listSources: List[NovelMetadata] = {
    FileSystemNovelsCSV.fromConfig.read
  }

  /* Load novel text.
   */
  def parse(source: NovelMetadata): Text = {
    FileSystemTextDir.fromConfig.mkText(source)
  }

}
