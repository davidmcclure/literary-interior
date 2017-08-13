

package lint.chicago


case class NovelMetadata(
  bookId: String,
  filename: String,
  title: String,
  authFirst: String,
  authLast: String,
  authId: String,
  publCity: String,
  publisher: String,
  publDate: Int,
  source: String,
  nationality: String,
  genre: String,
  clean: Boolean
)
