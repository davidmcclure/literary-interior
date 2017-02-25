

import org.apache.spark.{SparkContext,SparkConf}
import pprint.pprintln

import lint.config.Config


object TestConfig extends Config {

  val sc = new SparkContext(new SparkConf)

  def main(args: Array[String]) {

    val data = sc.parallelize(0 until 100)

    val res = data
      .map(i => {
        pprintln(config)
        i+1
      })
      .collect()

    pprintln(res)

  }

}
