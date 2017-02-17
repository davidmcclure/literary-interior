

package lint.config

import scala.util.{Success,Failure}
import pureconfig.loadConfig


case class LintConfig(gale: GaleConfig)
case class GaleConfig(directory: String)


trait Config {

  lazy val config = loadConfig[LintConfig] match {
    case Failure(f) => throw f
    case Success(conf) => conf
  }

}
