

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.{SparkSession,SaveMode}

import lint.config.Config
import lint.corpus.Novel


object LoadCorpus extends Config {

  val sc = new SparkContext(new SparkConf)
  val spark = SparkSession.builder.getOrCreate()
  import spark.implicits._

  def main(args: Array[String]) {

    // Read raw Gale + Chicago novels.

    val gale = spark.read
      .parquet(config.gale.novelParquet)
      .as[lint.gale.Novel]

    val chicago = spark.read
      .parquet(config.chicago.novelParquet)
      .as[lint.chicago.Novel]

    // Convert to normalized schema.
    val galeNovels = gale.map(Novel.fromGaleNovel)
    val chicagoNovels = chicago.map(Novel.fromChicagoNovel)

    // Merge into single dataset.
    val ds = galeNovels.union(chicagoNovels)

    ds.write.mode(SaveMode.Overwrite)
      .parquet(config.novelParquet)

    ds.show()

  }

}