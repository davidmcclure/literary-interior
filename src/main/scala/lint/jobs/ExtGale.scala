

import org.apache.spark.SparkContext
import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import scala.util.{Try,Success,Failure}

import lint.text._
import lint.gale._


object ExtGale {

  def main(args: Array[String]) {

    val conf = new SparkConf
    val sc = new SparkContext(conf)
    val spark = SparkSession.builder.getOrCreate()
    import spark.implicits._

    val texts = sc
      .parallelize(FileSystemLoader.listSources)
      .map(s => Try(FileSystemLoader.parse(s)))
      .filter {
        case Success(v) => true
        case Failure(e) => {
          println(e)
          false
        }
      }
      .map(_.get)

    val ds = spark.createDataset(texts)

    ds.write.parquet("gale.parquet")
    ds.show()
    println(ds.count())

  }

}
