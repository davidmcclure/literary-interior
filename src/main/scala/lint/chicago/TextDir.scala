

package lint.chicago

import java.nio.file.Paths
import scala.io.Source

import lint.utils.Tokenize
import lint.Config


class TextDir(val path: String) {

  /* Given a book ID, hydrate the text.
   */
  def readLines(filename: String): List[String] = {
    val textPath = Paths.get(path, filename).toString
    Source.fromFile(textPath).getLines.toList
  }

  /* Given a metadata row, build a text.
   */
  def mkNovel(row: NovelMetadata): Novel = {

    val lines = readLines(row.filename)

    val cleanLines = TextDir.stripGutenbergParatext(lines)

    val text = cleanLines.mkString("\n")

    val tokens = Tokenize(text)

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
      clean=row.clean,
      text=text,
      tokens=tokens
    )

  }

}


object TextDir extends Config {

  /* Bind config text path.
   */
  def fromConfig: TextDir = {
    new TextDir(config.chicago.textDir)
  }

  /* Strip out Project Gutenberg header / footer.
   */
  def stripGutenbergParatext(lines: List[String]): List[String] = {

    // By default, take all lines.
    var i1 = 0
    var i2 = lines.size

    val tokens = Set("***", "PROJECT", "GUTENBERG")

    val headerTokens = tokens + "START"
    val footerTokens = tokens + "END"

    // Probe for header / footer lines.
    for ((line, i) <- lines.zipWithIndex) {
      if (headerTokens.map(line.contains) == Set(true)) i1 = i+1
      if (footerTokens.map(line.contains) == Set(true)) i2 = i
    }

    // Slice off header / footer.
    lines.slice(i1, i2)

  }

}
