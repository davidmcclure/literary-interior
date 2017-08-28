

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
      KWICQuery("nose", 0, 0.05),
      KWICQuery("arms", 0.95, 1)
    )))

    // Write single JSON.
    matches
      .coalesce(1)
      .write
      .mode(SaveMode.Overwrite)
      .json(config.corpus.kwicBodyPartsJSON)

  }

}
