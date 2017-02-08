

package lint.tokenizer

import org.scalatest._
import pprint._


class TokenizerSpec extends FlatSpec with Matchers {

  "Tokenizer.tokenize()" should "POS-tag tokens" in {

    val tokens = Tokenizer.tokenize("My name is David.")

    tokens(0).token shouldEqual "my"
    tokens(0).pos shouldEqual "PRP$"

    tokens(1).token shouldEqual "name"
    tokens(1).pos shouldEqual "NN"

    tokens(2).token shouldEqual "is"
    tokens(2).pos shouldEqual "VBZ"

    tokens(3).token shouldEqual "david"
    tokens(3).pos shouldEqual "NNP"

  }

  it should "store character offsets" in {

    val tokens = Tokenizer.tokenize("12 34 56")

    tokens(0).token shouldEqual "12"
    tokens(0).start shouldEqual 0
    tokens(0).end shouldEqual 2

    tokens(1).token shouldEqual "34"
    tokens(1).start shouldEqual 3
    tokens(1).end shouldEqual 5

    tokens(2).token shouldEqual "56"
    tokens(2).start shouldEqual 6
    tokens(2).end shouldEqual 8

  }

  it should "store 0-1 ratio offsets" in {

    val tokens = Tokenizer.tokenize("1 2 3 4 5")

    tokens(0).token shouldEqual "1"
    tokens(0).offset shouldEqual 0

    tokens(1).token shouldEqual "2"
    tokens(1).offset shouldEqual 0.25

    tokens(2).token shouldEqual "3"
    tokens(2).offset shouldEqual 0.5

    tokens(3).token shouldEqual "4"
    tokens(3).offset shouldEqual 0.75

    tokens(4).token shouldEqual "5"
    tokens(4).offset shouldEqual 1

  }

  it should "downcase tokens" in {

    val tokens = Tokenizer.tokenize("MY NAME IS DAVID")

    tokens(0).token shouldEqual "my"
    tokens(1).token shouldEqual "name"
    tokens(2).token shouldEqual "is"
    tokens(3).token shouldEqual "david"

  }

}