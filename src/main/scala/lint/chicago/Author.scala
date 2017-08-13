

package lint.chicago


case class Author(
  authId: String,
  authLast: String,
  authFirst: String,
  altFirst: String,
  dateB: Option[Int],
  dateD: Option[Int],
  nationality: String,
  gender: String,
  race: String,
  hyphenatedIdentity: String,
  sexualIdentity: String,
  education: String,
  mfa: String,
  secondaryOccupation: String,
  coterie: String,
  religion: String,
  ses: String,
  geography: String
)
