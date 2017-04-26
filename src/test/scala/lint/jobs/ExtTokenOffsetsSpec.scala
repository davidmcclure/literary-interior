

package lint.jobs

import org.scalatest._
import org.scalatest.prop.TableDrivenPropertyChecks
import org.scalatest.prop.TableDrivenPropertyChecks._

import lint.corpus.{Novel,NovelFactory}
import lint.test.helpers.SparkTestSession


class ExtTokenOffsetsMergeOffsetsSpec extends FlatSpec with Matchers
  with SparkTestSession with TableDrivenPropertyChecks {

  "ExtBinCounts.mergeOffsets" should "combine offsets from novels" in {

    val spark = _spark
    import spark.implicits._

    val novels = Seq(

      NovelFactory(
        corpus="corpus1",
        identifier="1",
        title="title1",
        authorFirst="first1",
        authorLast="last1",
        year=1901,
        text="a b b"
      ),

      NovelFactory(
        corpus="corpus2",
        identifier="2",
        title="title2",
        authorFirst="first2",
        authorLast="last2",
        year=1902,
        text="a a b"
      ),

      NovelFactory(
        corpus="corpus3",
        identifier="3",
        title="title3",
        authorFirst="first3",
        authorLast="last3",
        year=1903,
        text="a a a"
      )

    )

    val ds = spark.createDataset(novels)

    val rows = ExtTokenOffsets.mergeOffsets(ds, "a")

    forAll(Table(
      ("novel", "offsets"),
      (novels(0), Seq(0.0)),
      (novels(1), Seq(0.0, 0.5)),
      (novels(2), Seq(0.0, 0.5, 1.0))
    )) { (
      novel: Novel,
      offsets: Seq[Double]
    ) =>

      val row = TokenOffsetsRow(
        corpus=novel.corpus,
        identifier=novel.identifier,
        title=novel.title,
        authorFirst=novel.authorFirst,
        authorLast=novel.authorLast,
        year=novel.year,
        offsets=offsets
      )

      rows.filter(_ == row).count shouldEqual 1

    }

  }

}
