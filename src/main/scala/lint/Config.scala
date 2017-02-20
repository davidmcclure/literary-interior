

package lint.config

import com.typesafe.config.ConfigFactory
import net.ceedubs.ficus.Ficus._
import net.ceedubs.ficus.readers.ArbitraryTypeReader._


case class LintConfig(gale: GaleConfig)
case class GaleConfig(directory: String)


trait Config {
  lazy val config = ConfigFactory.load.as[LintConfig]("lint")
}
