
import sbt._

object Dependencies {
  lazy val commonsio = "commons-io" % "commons-io" % "2.4"
  lazy val scalaxml = "org.scala-lang.modules" % "scala-xml_2.12" % "1.0.6"
  lazy val scalacsv = "com.github.tototoshi" %% "scala-csv" % "1.3.4"
  lazy val scalatest = "org.scalatest" %% "scalatest" % "3.0.1"
  lazy val awscala = "com.github.seratch" %% "awscala" % "0.5.9"
}
