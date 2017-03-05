
package lint.chicago


case class NovelMetadata(
  bookId: String,
  filename: String,
  title: String,
  authLast: String,
  authFirst: String,
  authId: String,
  publCity: String,
  publisher: String,
  publDate: Int,
  source: String,
  nationality: String,
  genre: String
)
