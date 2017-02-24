

package lint.chicago

import java.io.File
import java.nio.file.Paths
import scala.io.Source
import com.github.tototoshi.csv.CSVReader

import lint.config.Config
import lint.tokenizer.{Tokenizer,Token}
import lint.corpus.Text


case class NovelMetadata(
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
  genre: String,
  text: String,
  tokens: Seq[Token]
) extends Text


case class Author(
  authId: String,
  authLast: String,
  authFirst: String,
  altFirst: String,
  dateB: Option[Int],
  dateD: Option[Int],
  nationality: String,
  gender: String,
  raceEthnicity: String,
  hyphenatedIdentity: String,
  sexualIdentity: String,
  education: String,
  mfa: String,
  secondaryOccupation: String,
  coterie: String,
  religion: String,
  ses: String,
  geography: String
)


class NovelCSV(val path: String) {

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


object NovelCSV extends Config {

  /* Bind config novels CSV path.
   */
  def fromConfig: NovelCSV = {
    new NovelCSV(config.chicago.novelMetadataPath)
  }

}


class AuthorCSV(val path: String) {

  /* Map CSV rows into Author instances.
   */
  def read: List[Author] = {

    val reader = CSVReader.open(new File(path))

    for (row <- reader.allWithHeaders) yield {
      Author(
        authId=row("AUTH_ID"),
        authLast=row("AUTH_LAST"),
        authFirst=row("AUTH_FIRST"),
        altFirst=row("ALT_FIRST"),
        dateB=AuthorCSV.parseYear(row("DATE_B")),
        dateD=AuthorCSV.parseYear(row("DATE_D")),
        nationality=row("NATIONALITY"),
        gender=row("GENDER"),
        raceEthnicity=row("RACE_ETHNICITY"),
        hyphenatedIdentity=row("HYPHENATED_IDENTITY"),
        sexualIdentity=row("SEXUAL_IDENTITY"),
        education=row("EDUCATION"),
        mfa=row("MFA"),
        secondaryOccupation=row("SECONDARY_OCCUPATION"),
        coterie=row("COTERIE"),
        religion=row("RELIGION"),
        ses=row("CLASS"),
        geography=row("GEOGRAPHY")
      )
    }

  }

}


object AuthorCSV extends Config {

  /* Bind config novels CSV path.
   */
  def fromConfig: AuthorCSV = {
    new AuthorCSV(config.chicago.authorMetadataPath)
  }

  /* Clean a year string, case to integer.
   */
  def parseYear(year: String): Option[Int] = {
    "[0-9]{4}".r.findFirstIn(year) match {
      case Some(yearStr) => Some(yearStr.toInt)
      case None => None
    }
  }

}


class TextDir(val path: String) {

  /* Given a book ID, hydrate the text.
   */
  def read(filename: String): String = {
    val textPath = Paths.get(path, filename).toString
    Source.fromFile(textPath).getLines.mkString
  }

  /* Given a metadata row, build a text.
   */
  def mkNovel(row: NovelMetadata): Novel = {

    val text = read(row.filename)
    val tokens = Tokenizer.tokenize(text)

    Novel(
      bookId=row.bookId,
      filename=row.filename,
      title=row.title,
      authLast=row.authLast,
      authFirst=row.authFirst,
      authId=row.authId,
      publCity=row.publCity,
      publisher=row.publisher,
      publDate=row.publDate,
      source=row.source,
      nationality=row.nationality,
      genre=row.genre,
      text=text,
      tokens=tokens
    )

  }

}


object TextDir extends Config {

  /* Bind config text path.
   */
  def fromConfig: TextDir = {
    new TextDir(config.chicago.textDirectory)
  }

}


object Loader {

  /* List novel metadata rows.
   */
  def sources: List[NovelMetadata] = {
    NovelCSV.fromConfig.read.slice(0, 20) // TODO|dev
  }

  /* Load novel text.
   */
  def parse(source: NovelMetadata): Novel = {
    TextDir.fromConfig.mkNovel(source)
  }

}
