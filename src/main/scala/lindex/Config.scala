

package lindex.config

import com.typesafe.config.ConfigFactory
import net.ceedubs.ficus.Ficus._
import net.ceedubs.ficus.readers.ArbitraryTypeReader._


case class LindexConfig(
  gale: GaleConfig,
  chicago: ChicagoConfig,
  novelParquet: String
)

case class GaleConfig(
  corpusDir: String,
  novelParquet: String
)

case class ChicagoConfig(
  novelMetadataPath: String,
  authorMetadataPath: String,
  textDir: String,
  novelParquet: String,
  authorParquet: String
)


trait Config {
  lazy val config = ConfigFactory.load.as[LindexConfig]("lindex")
}
