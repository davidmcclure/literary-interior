
import sbt._

object Dependencies {

  lazy val commonsio = "commons-io" % "commons-io" % "2.4"
  lazy val scalaxml = "org.scala-lang.modules" % "scala-xml_2.11" % "1.0.6"
  lazy val scalacsv = "com.github.tototoshi" %% "scala-csv" % "1.3.4"
  lazy val pprint = "com.lihaoyi" %% "pprint" % "0.4.3"

  lazy val spark = "org.apache.spark" %% "spark-core" % "2.1.0" % "provided"
  lazy val sparksql = "org.apache.spark" %% "spark-sql" % "2.1.0" % "provided"

  lazy val scalatest = "org.scalatest" %% "scalatest" % "3.0.1"

}
