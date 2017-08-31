

package lint.corpus


case class KWICQuery(
  token: String,
  minOffset: Double = 0,
  maxOffset: Double = 100,
  radius: Int = 500
)
