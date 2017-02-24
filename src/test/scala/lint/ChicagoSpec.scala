

package lint.chicago

import org.scalatest._


class NovelsCSVSpec extends FreeSpec with Matchers {

  val url = getClass().getResource("/fixtures/chicago/NOVELS_METADATA.csv")
  val reader = new NovelsCSV(url.getFile)

  "CSV should parse without errors" in {
    val rows = reader.read
    rows.size should be > 0
  }

}
