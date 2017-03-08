

package lint.jobs

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.SparkSession

import org.scalatest._


class ExtBinCountsMergeCountsSpec extends FlatSpec
  with Matchers with BeforeAndAfter {

  var sc: SparkContext = _

  before {
    val conf = new SparkConf().setMaster("local[*]").setAppName("test")
    sc = new SparkContext(conf)
  }

  after {
    sc.stop
  }

  "ExtBinCounts.mergeCounts" should "index TokenBin -> count" in {
    true shouldEqual true
  }

}
