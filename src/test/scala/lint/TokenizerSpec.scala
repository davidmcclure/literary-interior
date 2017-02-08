

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

  it should "track character offsets across sentences" in {

    val tokens = Tokenizer.tokenize("I walk. She runs. He strolls.")

    tokens(0).token shouldEqual "i"
    tokens(0).start shouldEqual 0
    tokens(0).end shouldEqual 1

    tokens(1).token shouldEqual "walk"
    tokens(1).start shouldEqual 2
    tokens(1).end shouldEqual 6

    tokens(2).token shouldEqual "."
    tokens(2).start shouldEqual 6
    tokens(2).end shouldEqual 7

    tokens(3).token shouldEqual "she"
    tokens(3).start shouldEqual 8
    tokens(3).end shouldEqual 11

    tokens(4).token shouldEqual "runs"
    tokens(4).start shouldEqual 12
    tokens(4).end shouldEqual 16

    tokens(5).token shouldEqual "."
    tokens(5).start shouldEqual 16
    tokens(5).end shouldEqual 17

    tokens(6).token shouldEqual "he"
    tokens(6).start shouldEqual 18
    tokens(6).end shouldEqual 20

    tokens(7).token shouldEqual "strolls"
    tokens(7).start shouldEqual 21
    tokens(7).end shouldEqual 28

    tokens(8).token shouldEqual "."
    tokens(8).start shouldEqual 28
    tokens(8).end shouldEqual 29

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

  it should "track 0-1 ratio offsets across sentences" in {

    val tokens = Tokenizer.tokenize("I walk. She runs. He strolls.")

    tokens(0).token shouldEqual "i"
    tokens(0).offset shouldEqual 0

    tokens(1).token shouldEqual "walk"
    tokens(1).offset shouldEqual 0.125

    tokens(2).token shouldEqual "."
    tokens(2).offset shouldEqual 0.25

    tokens(3).token shouldEqual "she"
    tokens(3).offset shouldEqual 0.375

    tokens(4).token shouldEqual "runs"
    tokens(4).offset shouldEqual 0.5

    tokens(5).token shouldEqual "."
    tokens(5).offset shouldEqual 0.625

    tokens(6).token shouldEqual "he"
    tokens(6).offset shouldEqual 0.75

    tokens(7).token shouldEqual "strolls"
    tokens(7).offset shouldEqual 0.875

    tokens(8).token shouldEqual "."
    tokens(8).offset shouldEqual 1

  }

  it should "downcase tokens" in {

    val tokens = Tokenizer.tokenize("My Name Is David.")

    tokens(0).token shouldEqual "my"
    tokens(1).token shouldEqual "name"
    tokens(2).token shouldEqual "is"
    tokens(3).token shouldEqual "david"

  }

}
