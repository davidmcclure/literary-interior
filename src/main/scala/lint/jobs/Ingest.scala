

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.{SparkSession,SaveMode}
import scala.util.{Try,Success,Failure}
import java.io.File

import lint.chicago.NovelMetadata


object Ingest {

  val sc = new SparkContext(new SparkConf)
  val spark = SparkSession.builder.getOrCreate()
  import spark.implicits._

  def main(args: Array[String]) {

    val chicago = ingest[NovelMetadata](lint.chicago.FileSystemLoader)
    val gale = ingest[File](lint.gale.FileSystemLoader)

    println(gale)

  }

  def ingest[T](implicit loader: lint.corpus.Loader[T]) = {

    val texts = sc.parallelize(loader.listSources)

      // Parse sources.
      .map(s => Try(loader.parse(s)))

      // Log + prune errors.
      .filter {
        case Success(v) => true
        case Failure(e) => println(e); false;
      }

      // Get results.
      .map(_.get)

    spark.createDataset(texts)

  }

}
