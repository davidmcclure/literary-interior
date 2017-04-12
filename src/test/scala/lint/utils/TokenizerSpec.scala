

package lint.utils

import org.scalatest._
import org.scalatest.prop.TableDrivenPropertyChecks
import org.scalatest.prop.TableDrivenPropertyChecks._


class TokenizeSpec extends FlatSpec with Matchers
  with TableDrivenPropertyChecks {

  "Tokenize()" should "POS-tag tokens" in {

    val tokens = Tokenize("My name is David.")

    forAll(Table(

      ("index", "token", "pos"),

      (0, "my", "PRP$"),
      (1, "name", "NN"),
      (2, "is", "VBZ"),
      (3, "david", "NNP")

    )) { (index: Int, token: String, pos: String) =>
      tokens(index).token shouldEqual token
      tokens(index).pos shouldEqual pos
    }

  }

  it should "store character offsets" in {

    val tokens = Tokenize("12 34 56")

    forAll(Table(

      ("index", "token", "start", "end"),

      (0, "12", 0, 2),
      (1, "34", 3, 5),
      (2, "56", 6, 8)

    )) { (index: Int, token: String, start: Int, end: Int) =>
      tokens(index).token shouldEqual token
      tokens(index).start shouldEqual start
      tokens(index).end shouldEqual end
    }

  }

  it should "track character offsets across sentences" in {

    val tokens = Tokenize("I walk. She runs. He strolls.")

    forAll(Table(

      ("index", "token", "start", "end"),

      (0, "i", 0, 1),
      (1, "walk", 2, 6),
      (2, ".", 6, 7),
      (3, "she", 8, 11),
      (4, "runs", 12, 16),
      (5, ".", 16, 17),
      (6, "he", 18, 20),
      (7, "strolls", 21, 28),
      (8, ".", 28, 29)

    )) { (index: Int, token: String, start: Int, end: Int) =>
      tokens(index).token shouldEqual token
      tokens(index).start shouldEqual start
      tokens(index).end shouldEqual end
    }

  }

  it should "store 0-1 ratio offsets" in {

    val tokens = Tokenize("1 2 3 4 5")

    forAll(Table(

      ("index", "token", "offset"),

      (0, "1", 0.0),
      (1, "2", 0.25),
      (2, "3", 0.5),
      (3, "4", 0.75),
      (4, "5", 1.0)

    )) { (index: Int, token: String, offset: Double) =>
      tokens(index).token shouldEqual token
      tokens(index).offset shouldEqual offset
    }

  }

  it should "track 0-1 ratio offsets across sentences" in {

    val tokens = Tokenize("I walk. She runs. He strolls.")

    forAll(Table(

      ("index", "token", "offset"),

      (0, "i", 0.0),
      (1, "walk", 0.125),
      (2, ".", 0.25),
      (3, "she", 0.375),
      (4, "runs", 0.5),
      (5, ".", 0.625),
      (6, "he", 0.75),
      (7, "strolls", 0.875),
      (8, ".", 1.0)

    )) { (index: Int, token: String, offset: Double) =>
      tokens(index).token shouldEqual token
      tokens(index).offset shouldEqual offset
    }

  }

  it should "downcase tokens" in {

    val tokens = Tokenize("My Name Is David.")

    forAll(Table(

      ("index", "token"),

      (0, "my"),
      (1, "name"),
      (2, "is"),
      (3, "david")

    )) { (index: Int, token: String) =>
      tokens(index).token shouldEqual token
    }

  }

}
