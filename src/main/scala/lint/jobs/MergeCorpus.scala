

package lint.jobs

import org.apache.spark.sql.{SparkSession,SaveMode}

import lint.Config
import lint.corpus.Novel


object MergeCorpus extends Config {

  lazy val spark = SparkSession.builder.getOrCreate()
  import spark.implicits._

  def main(args: Array[String]) {

    // Read raw Gale novels.
    val gale = spark.read
      .parquet(config.gale.novelParquet)
      .as[lint.gale.Novel]

    // Read raw Chicago novels.
    val chicago = spark.read
      .parquet(config.chicago.novelParquet)
      .as[lint.chicago.Novel]

    // Convert to normalized schema.
    val galeNovels = gale.map(Novel.fromGaleNovel)
    val chicagoNovels = chicago.map(Novel.fromChicagoNovel)

    // Merge into single dataset.
    val ds = galeNovels.union(chicagoNovels)

    ds.write.mode(SaveMode.Overwrite)
      .parquet(config.corpus.novelParquet)

  }

}
