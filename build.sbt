
import Dependencies._

lazy val root = (project in file(".")).
  settings(

    inThisBuild(List(
      organization := "edu.lint",
      scalaVersion := "2.12.1",
      version      := "0.1.0-SNAPSHOT"
    )),

    name := "lint",

    libraryDependencies ++= Seq(
      commonsIO,
      scalaXML,
      scalaCSV,
      scalaTest % Test
    )

  )
