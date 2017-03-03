

package lindex.jobs

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.{SparkSession,SaveMode}

import lindex.config.Config
import lindex.corpora.literaryinterior.Novel


object LoadLiteraryInterior extends Job with Config {

  import spark.implicits._

  def main(args: Array[String]) {

    // Read raw Gale + Chicago novels.

    val gale = spark.read
      .parquet(config.gale.novelParquet)
      .as[lindex.corpora.gale.Novel]

    val chicago = spark.read
      .parquet(config.chicago.novelParquet)
      .as[lindex.corpora.chicago.Novel]

    // Convert to normalized schema.
    val galeNovels = gale.map(Novel.fromGaleNovel)
    val chicagoNovels = chicago.map(Novel.fromChicagoNovel)

    // Merge into single dataset.
    val ds = galeNovels.union(chicagoNovels)

    ds.write.mode(SaveMode.Overwrite)
      .parquet(config.novelParquet)

    ds.show

  }

}
