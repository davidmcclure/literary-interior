

package lint.config

import com.typesafe.config.ConfigFactory
import net.ceedubs.ficus.Ficus._
import net.ceedubs.ficus.readers.ArbitraryTypeReader._


case class LintConfig(
  gale: GaleConfig,
  chicago: ChicagoConfig
)

case class GaleConfig(
  directory: String
)

case class ChicagoConfig(
  novelMetadataPath: String,
  authorMetadataPath: String,
  textDirectory: String
)


// TODO: Inject with MacWire?
trait Config {
  lazy val config = ConfigFactory.load.as[LintConfig]("lint")
}
