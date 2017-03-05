

package lint.gale

import java.io.File


object Loader {

  /* List XML paths.
   */
  def sources: List[File] = {
    Corpus.fromConfig.listPaths.toList.slice(0, 100) // TODO|dev
  }

  /* XML -> Text.
   */
  def parse(source: File): Novel = {
    NovelXML.fromFile(source).mkNovel
  }

}
