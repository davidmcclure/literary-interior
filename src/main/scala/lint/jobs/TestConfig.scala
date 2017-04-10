

package lint.jobs

import org.apache.spark.{SparkContext,SparkConf}
import pprint.pprintln

import lint.Config


object TestConfig extends Config {

  lazy val sc = new SparkContext(new SparkConf)

  def main(args: Array[String]) {

    val data = sc.parallelize(0 until 100)

    val res = data
      .map(i => config.chicago.textDir)
      .collect()

    pprintln(res)

  }

}
