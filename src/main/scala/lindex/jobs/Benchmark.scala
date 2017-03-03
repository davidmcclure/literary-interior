

package lindex.jobs

import org.apache.spark.{SparkContext,SparkConf}
import pprint.pprintln


object Benchmark extends Job {

  def main(args: Array[String]) {

    val data = sc.parallelize(0 until 100)

    val res = data
      .map(i => {
        new Thread
        Thread.sleep(1000)
        i+1
      })
      .collect()

    pprintln(res)

  }

}
