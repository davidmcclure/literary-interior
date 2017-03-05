

package lint.chicago

import java.nio.file.Paths
import scala.io.Source

import lint.tokenizer.Tokenizer
import lint.config.Config


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

    // TODO: Strip Gutenberg header / footer.

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
    new TextDir(config.chicago.textDir)
  }

}
