

//import org.apache.spark.{SparkContext,SparkConf}
//import org.apache.spark.sql.{SparkSession,SaveMode}
//import scala.util.{Try,Success,Failure}

//import lint.gale.FileSystemLoader


//object ExtGale {

  //def main(args: Array[String]) {

    //val sc = new SparkContext(new SparkConf)
    //val spark = SparkSession.builder.getOrCreate()
    //import spark.implicits._

    //val texts = sc

      //// Parse sources.
      //.parallelize(FileSystemLoader.listSources)
      //.map(s => Try(FileSystemLoader.parse(s)))

      //// Log + prune errors.
      //.filter {
        //case Success(v) => true
        //case Failure(e) => println(e); false;
      //}

      //// Get results.
      //.map(_.get)

    //val ds = spark.createDataset(texts)

    //ds.write.mode(SaveMode.Overwrite).parquet("gale.parquet")
    //ds.show()

  //}

//}
