

package lint.chicago

import lint.utils.Token


case class Novel(
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
  genre: String,
  clean: Boolean,
  text: String,
  tokens: Seq[Token]
)
