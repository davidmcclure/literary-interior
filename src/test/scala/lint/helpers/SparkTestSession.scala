

package lint.test.helpers

import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession

import org.scalatest._


trait SparkTestSession extends BeforeAndAfterAll { self: Suite =>

  var _spark: SparkSession = _

  override def beforeAll {

    val conf = new SparkConf()
      .setMaster("local[*]")
      .setAppName("test")

    _spark = SparkSession.builder
      .config(conf)
      .getOrCreate()

  }

  override def afterAll {
    _spark.stop
  }

}
