

package lint.gale

import org.scalatest._


class NovelSpec extends FlatSpec with Matchers {

  "Novel.identifier()" should "provide the PSMID" in {
    val novel = new Novel(<PSMID>1</PSMID>)
    novel.identifier shouldEqual "1"
  }

}
