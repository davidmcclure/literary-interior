
import sbt._

object Dependencies {

  lazy val commonsIO =
    "commons-io" % "commons-io" % "2.4"

  lazy val scalaXML =
    "org.scala-lang.modules" % "scala-xml_2.11" % "1.0.6"

  lazy val scalaCSV =
    "com.github.tototoshi" %% "scala-csv" % "1.3.4"

  lazy val spark =
    "org.apache.spark" %% "spark-core" % "2.1.0" % "provided"

  lazy val sparkSQL =
    "org.apache.spark" %% "spark-sql" % "2.1.0" % "provided"

  lazy val pprint =
    "com.lihaoyi" %% "pprint" % "0.4.3"

  lazy val scalaTest =
    "org.scalatest" %% "scalatest" % "3.0.1"

}
