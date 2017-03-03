

package lindex.jobs

import org.apache.spark.{SparkContext,SparkConf}
import org.apache.spark.sql.{SparkSession,SaveMode}


trait Job {
  lazy val sc = new SparkContext(new SparkConf)
  lazy val spark = SparkSession.builder.getOrCreate()
}
