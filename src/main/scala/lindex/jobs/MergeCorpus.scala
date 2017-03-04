

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.{SparkSession,SaveMode}

import lindex.config.Config
import lindex.corpus.Novel


object MergeCorpus extends Config {

  val sc = new SparkContext(new SparkConf)
  val spark = SparkSession.builder.getOrCreate()
  import spark.implicits._

  def main(args: Array[String]) {

    // Read raw Gale novels.
    val gale = spark.read
      .parquet(config.gale.novelParquet)
      .as[lindex.gale.Novel]

    // Read raw Chicago novels.
    val chicago = spark.read
      .parquet(config.chicago.novelParquet)
      .as[lindex.chicago.Novel]

    // Convert to normalized schema.
    val galeNovels = gale.map(Novel.fromGaleNovel)
    val chicagoNovels = chicago.map(Novel.fromChicagoNovel)

    // Merge into single dataset.
    val ds = galeNovels.union(chicagoNovels)

    ds.write.mode(SaveMode.Overwrite)
      .parquet(config.literaryinterior.novelParquet)

    ds.show

  }

}
