

package lint.jobs

import org.scalatest._
import org.scalatest.prop.TableDrivenPropertyChecks
import org.scalatest.prop.TableDrivenPropertyChecks._

import lint.utils.Tokenize
import lint.corpus.NovelFactory
import lint.test.helpers.SparkTestSession


class ExtTokenOffsetsMergeOffsetsSpec extends FlatSpec with Matchers
  with SparkTestSession with TableDrivenPropertyChecks {

  "ExtBinCounts.mergeOffsets" should "combine offsets from novels" in {

    val spark = _spark
    import spark.implicits._

    val novels = spark.createDataset(Seq(

      NovelFactory(
        corpus="corpus1",
        identifier="1",
        title="title1",
        year=1901,
        text="a b b"
      ),

      NovelFactory(
        corpus="corpus2",
        identifier="2",
        title="title2",
        year=1902,
        text="a a b"
      ),

      NovelFactory(
        corpus="corpus3",
        identifier="3",
        title="title3",
        year=1903,
        text="a a a"
      )

    ))

    val rows = ExtTokenOffsets.mergeOffsets(novels, "a")

    forAll(Table(
      ("corpus", "identifier", "title", "year", "offsets"),
      ("corpus1", "1", "title1", 1901, Seq(0.0)),
      ("corpus2", "2", "title2", 1902, Seq(0.0, 0.5)),
      ("corpus3", "3", "title3", 1903, Seq(0.0, 0.5, 1.0))
    )) { (
      corpus: String,
      identifier: String,
      title: String,
      year: Int,
      offsets: Seq[Double]
    ) =>

      val row = TokenOffsetsRow(corpus, identifier, title, year, offsets)
      rows.filter(_ == row).count shouldEqual 1

    }

  }

}
