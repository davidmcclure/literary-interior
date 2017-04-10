

package lint.chicago

import java.io.File
import com.github.tototoshi.csv.CSVReader

import lint.Config


class AuthorCSV(val path: String) {

  /* Map CSV rows into Author instances.
   */
  def read: List[Author] = {

    val reader = CSVReader.open(new File(path))

    for (row <- reader.allWithHeaders) yield Author(
      authId=row("AUTH_ID"),
      authLast=row("AUTH_LAST"),
      authFirst=row("AUTH_FIRST"),
      altFirst=row("ALT_FIRST"),
      dateB=AuthorCSV.parseYear(row("DATE_B")),
      dateD=AuthorCSV.parseYear(row("DATE_D")),
      nationality=row("NATIONALITY"),
      gender=row("GENDER"),
      raceEthnicity=row("RACE_ETHNICITY"),
      hyphenatedIdentity=row("HYPHENATED_IDENTITY"),
      sexualIdentity=row("SEXUAL_IDENTITY"),
      education=row("EDUCATION"),
      mfa=row("MFA"),
      secondaryOccupation=row("SECONDARY_OCCUPATION"),
      coterie=row("COTERIE"),
      religion=row("RELIGION"),
      ses=row("CLASS"),
      geography=row("GEOGRAPHY")
    )

  }

}


object AuthorCSV extends Config {

  /* Bind config novels CSV path.
   */
  def fromConfig: AuthorCSV = {
    new AuthorCSV(config.chicago.authorCSVPath)
  }

  /* Clean a year string, case to integer.
   */
  def parseYear(year: String): Option[Int] = {
    "[0-9]{4}".r.findFirstIn(year) match {
      case Some(yearStr) => Some(yearStr.toInt)
      case None => None
    }
  }

}
