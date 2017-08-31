

package lint.jobs

import org.apache.spark.sql.{SparkSession,SaveMode}

import lint.Config
import lint.corpus.{Novel,KWICQuery}


object KWICBodyParts extends Config {

  lazy val spark = SparkSession.builder.getOrCreate()
  import spark.implicits._

  /* Body part KWICs.
   */
  def main(args: Array[String]) {

    // Read novels.
    val novels = spark.read
      .parquet(config.corpus.novelParquet)
      .as[Novel]

    // Probe for query matches.
    val matches = novels.flatMap(novel => novel.kwics(Seq(
      KWICQuery("hair", 0, 0.05),
      KWICQuery("hair", 0.95, 1),
      KWICQuery("curls", 0, 0.05),
      KWICQuery("curls", 0.95, 1),
      KWICQuery("heart", 0.95, 1),
      KWICQuery("hearts", 0.95, 1),
      KWICQuery("arms", 0.95, 1),
      KWICQuery("arm", 0.95, 1),
      KWICQuery("nose", 0, 0.05),
      KWICQuery("hands", 0.95, 1),
      KWICQuery("eyes", 0, 0.05),
      KWICQuery("eyes", 0.95, 1),
      KWICQuery("eye", 0, 0.05),
      KWICQuery("face", 0, 0.05),
      KWICQuery("face", 0.95, 1),
      KWICQuery("body", 0.9, 1),
      KWICQuery("skin", 0, 0.05),
      KWICQuery("chin", 0, 0.05),
      KWICQuery("breast", 0.95, 1),
      KWICQuery("blood", 0.9, 1),
      KWICQuery("lips", 0.95, 1),
      KWICQuery("mustache", 0, 0.05),
      KWICQuery("eyebrows", 0, 0.05),
      KWICQuery("brows", 0, 0.05)
    )))

    // Write single JSON.
    matches
      .write
      .mode(SaveMode.Overwrite)
      .json(config.corpus.kwicBodyPartsJSON)

  }

}
