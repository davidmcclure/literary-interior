

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf


object Test {

  def main(args: Array[String]) {

    val conf = new SparkConf().setAppName("test")
    val sc = new SparkContext(conf)

    val readme = sc.textFile("README.md")

    val wordcount = readme
      .flatMap(line => line.split(" "))
      .map(word => (word, 1))
      .reduceByKey((a, b) => a+b)

    println(wordcount.collect().toMap)
    sc.stop()

  }

}
