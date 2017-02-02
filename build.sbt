
import Dependencies._

lazy val root = (project in file(".")).
  settings(

    inThisBuild(List(
      organization := "edu.lint",
      scalaVersion := "2.11.8",
      version      := "0.1.0-SNAPSHOT"
    )),

    name := "lint",

    libraryDependencies ++= Seq(
      commonsio,
      spark,
      scalaxml,
      scalacsv,
      pprint,
      scalatest % Test
    ),

    assemblyJarName in assembly := "lint.jar"

  )
