

package lint.chicago


object NovelMetadataFactory {

  def apply(

    bookId: String = "1",
    filename: String = "1.txt",
    title: String = "title",
    authFirst: String = "first",
    authLast: String = "last",
    authId: String = "1",
    publCity: String = "city",
    publisher: String = "publisher",
    publDate: Int = 2000,
    source: String = "source",
    nationality: String = "nationality",
    genre: String = "genre",
    clean: Boolean = true

  ) = NovelMetadata(

    bookId=bookId,
    filename=filename,
    title=title,
    authFirst=authFirst,
    authLast=authLast,
    authId=authId,
    publCity=publCity,
    publisher=publisher,
    publDate=publDate,
    source=source,
    nationality=nationality,
    genre=genre,
    clean=clean

  )

}
