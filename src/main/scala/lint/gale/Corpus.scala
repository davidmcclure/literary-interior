

package lint.gale

import java.io.File

import lint.utils.FileSystem
import lint.config.Config


class Corpus(private val path: String) {

  val root = new File(path)

  /* Recursively list XML sources.
   */
  def listPaths = {
    FileSystem.walkTree(root).filter(_.toString.endsWith(".xml"))
  }

}


object Corpus extends Config {

  /* Read corpus root from config.
   */
  def fromConfig: Corpus = {
    new Corpus(config.gale.corpusDir)
  }

}
