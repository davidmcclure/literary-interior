

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.{SparkSession,SaveMode}
import scala.util.{Try,Success,Failure}

import lint.chicago.FileSystemNovelsCSV


object ExtChicago {

  def main(args: Array[String]) {

    val sc = new SparkContext(new SparkConf)
    val spark = SparkSession.builder.getOrCreate()
    import spark.implicits._

    val novels = FileSystemNovelsCSV.fromConfig.read
    val ds = spark.createDataset(novels)

    ds.write.mode(SaveMode.Overwrite).parquet("chicago.parquet")
    ds.show()

  }

}

