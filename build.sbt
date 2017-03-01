
import Dependencies._

lazy val root = (project in file("."))
  .settings(

    inThisBuild(List(
      organization := "edu.lint",
      scalaVersion := "2.11.8",
      version      := "0.1.0-SNAPSHOT"
    )),

    name := "lint",

    libraryDependencies ++= Seq(
      ficus,
      commonsIO,
      scalaXML,
      scalaCSV,
      sparkCore,
      sparkSQL,
      pprint,
      openNLP,
      scopt,
      scalaTest % Test
    ),

    assemblyJarName in assembly := "lint.jar"

  )
