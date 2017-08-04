

package lint

import com.typesafe.config.ConfigFactory
import net.ceedubs.ficus.Ficus._
import net.ceedubs.ficus.readers.ArbitraryTypeReader._


case class LintConfig(
  gale: GaleConfig,
  chicago: ChicagoConfig,
  corpus: CorpusConfig
)

case class GaleConfig(
  corpusDir: String,
  novelParquet: String
)

case class ChicagoConfig(
  novelCSVPath: String,
  authorCSVPath: String,
  textDir: String,
  novelParquet: String,
  authorParquet: String
)

case class CorpusConfig(
  novelParquet: String,
  binCountJSON: String
)


trait Config {
  lazy val config = ConfigFactory.load.as[LintConfig]("lint")
}
