

package lint.chicago


object Loader {

  /* List novel metadata rows.
   */
  def sources: List[NovelMetadata] = {
    NovelCSV.fromConfig.read.slice(0, 100) // TODO|dev
  }

  /* Load novel text.
   */
  def parse(source: NovelMetadata): Novel = {
    TextDir.fromConfig.mkNovel(source)
  }

}
