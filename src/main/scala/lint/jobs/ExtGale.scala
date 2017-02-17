

import scala.util.{Try,Success,Failure}
import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.{SparkSession,SaveMode}

import lint.corpus._
import lint.gale.Corpus


object ExtGale {

  def main(args: Array[String]) {

    val c = Corpus.fromConfig
    println(c.listPaths)

    //val conf = new SparkConf
    //val sc = new SparkContext(conf)
    //val spark = SparkSession.builder.getOrCreate()
    //import spark.implicits._

    //val texts = sc
      //.parallelize(FileSystemLoader.listSources)
      //.map(s => Try(FileSystemLoader.parse(s)))
      //.filter {
        //case Success(v) => true
        //case Failure(e) => println(e); false;
      //}
      //.map(_.get)

    //val ds = spark.createDataset(texts)

    //ds.write.mode(SaveMode.Overwrite).parquet("gale.parquet")
    //ds.show()

  }

}
