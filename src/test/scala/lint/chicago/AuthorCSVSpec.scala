

package lint.chicago

import org.scalatest._


class AuthorCSVSpec extends FreeSpec with Matchers {

  val url = getClass().getResource("/fixtures/chicago/AUTHORS_METADATA.csv")
  val reader = new AuthorCSV(url.getFile)

  "CSV should parse without errors" in {
    val rows = reader.read
    rows.size should be > 0
  }

  // TODO: Spot-check rows.

}