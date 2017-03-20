

package lint.chicago


object Loader {

  /* List novel metadata rows.
   */
  def sources: List[NovelMetadata] = {
    NovelCSV.fromConfig.read
  }

  /* Load novel text.
   */
  def parse(source: NovelMetadata): Novel = {
    TextDir.fromConfig.mkNovel(source)
  }

}
