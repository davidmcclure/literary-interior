

package lint.chicago

import java.io.File
import java.nio.file.Paths
import scala.io.Source
import com.github.tototoshi.csv.CSVReader
import lint.config.Config
import lint.corpus.{Text,Loader}


case class Novel(
  bookId: String,
  filename: String,
  title: String,
  authLast: String,
  authFirst: String,
  authId: String,
  publCity: String,
  publisher: String,
  publDate: Int,
  source: String,
  nationality: String,
  genre: String
)


class FileSystemNovelsCSV(val path: String) {

  /* Map CSV rows into Novel instances.
   */
  def read: List[Novel] = {

    val reader = CSVReader.open(new File(path))

    for (row <- reader.allWithHeaders) yield {
      Novel(
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

}


object FileSystemNovelsCSV extends Config {

  /* Bind config novels CSV path.
   */
  def fromConfig: FileSystemNovelsCSV = {
    new FileSystemNovelsCSV(config.chicago.novelMetadataPath)
  }

}


//class FileSystemTextDir(val path: String) {

  /* Given a book ID, hydrate the text.
   */
  //def read(filename: String): String = {
    //val textPath = Paths.get(path, filename).toString
    //Source.fromFile(textPath).getLines.mkString
  //}

  /* Given a metadata row, build a text.
   */
  //def mkText(row: Novel): Text = {
    //Text(
      //corpus="chicago",
      //identifier=row.bookId,
      //title=row.title,
      //authorFirst=Some(row.authFirst),
      //authorLast=Some(row.authLast),
      //year=row.publDate,
      //text=read(row.filename)
    //)
  //}

//}


//object FileSystemTextDir extends Config {

  /* Bind config text path.
   */
  //def fromConfig: FileSystemTextDir = {
    //new FileSystemTextDir(config.chicago.textDirectory)
  //}

//}


//object FileSystemLoader extends Loader[NovelMetadata] {

  /* List novel metadata rows.
   */
  //def listSources: List[NovelMetadata] = {
    //FileSystemNovelsCSV.fromConfig.read.slice(0, 20) // TODO|dev
  //}

  /* Load novel text.
   */
  //def parse(source: NovelMetadata): Text = {
    //FileSystemTextDir.fromConfig.mkText(source)
  //}

//}
