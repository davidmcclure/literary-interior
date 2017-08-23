

package lint.chicago

import org.scalatest._


class AuthorCSVSpec extends FreeSpec with Matchers {

  val file = new java.io.File(
    "/fixtures/chicago/CHICAGO_NOVEL_CORPUS_METADATA",
    "CHICAGO_CORPUS_AUTHORS.csv"
  )

  val url = getClass().getResource(file.toString)

  val reader = new AuthorCSV(url.getFile)

  "CSV should parse without errors" in {
    val rows = reader.read
    rows.size should be > 0
  }

  // TODO: Spot-check rows.

}
