import sbt._

object Dependencies {
  lazy val commonsIO = "commons-io" % "commons-io" % "2.4"
  lazy val scalaXML = "org.scala-lang.modules" % "scala-xml_2.12" % "1.0.6"
  lazy val scalaCSV = "com.github.tototoshi" %% "scala-csv" % "1.3.4"
  lazy val scalaTest = "org.scalatest" %% "scalatest" % "3.0.1"
}
