

import click

from pyspark.sql.functions import lit

from lint.utils import get_spark
from lint.models import Novel


@click.command()
@click.argument('gale_src', type=click.Path())
@click.argument('chicago_novels_src', type=click.Path())
@click.argument('chicago_authors_src', type=click.Path())
@click.argument('dest', type=click.Path())
def main(gale_src, chicago_novels_src, chicago_authors_src, dest):
    """Ingest Gale.
    """
    sc, spark = get_spark()

    gale = spark.read.parquet(gale_src)

    chicago_novels = spark.read.parquet(chicago_novels_src)
    chicago_authors = spark.read.parquet(chicago_authors_src)

    # Columns in authors but not novels.
    diff_cols = set.difference(
        set(chicago_authors.columns),
        set(chicago_novels.columns),
    )

    # Join authors onto novels.
    chicago_authors = chicago_authors.select('auth_id', *diff_cols)
    chicago = chicago_novels.join(chicago_authors, 'auth_id')

    gale_unified = gale.select(
        lit('gale').alias('corpus'),
        gale.psmid.alias('identifier'),
        gale.full_title.alias('title'),
        gale.author_last,
        gale.author_first,
        gale.pub_date_start.alias('pub_year'),
        gale.language.alias('gale_language'),
        gale.ocr.alias('gale_ocr'),
        gale.text,
    )

    chicago_unified = chicago.select(
        lit('chicago').alias('corpus'),
        chicago.book_id.alias('identifier'),
        chicago.title,
        chicago.auth_last.alias('author_last'),
        chicago.auth_first.alias('author_first'),
        chicago.publ_date.alias('pub_year'),
        chicago.libraries.alias('chicago_libraries'),
        chicago.publ_city.alias('chicago_publ_city'),
        chicago.publisher.alias('chicago_publisher'),
        chicago.source.alias('chicago_source'),
        chicago.nationality.alias('chicago_nationality'),
        chicago.genre.alias('chicago_genre'),
        chicago.clean.alias('chicago_clean'),
        chicago.auth_id.alias('chicago_auth_id'),
        chicago.canon.alias('chicago_auth_canon'),
        chicago.date_b.alias('chicago_auth_date_b'),
        chicago.date_d.alias('chicago_auth_date_d'),
        chicago.nationality.alias('chicago_auth_nationality'),
        chicago.gender.alias('chicago_auth_gender'),
        chicago.race.alias('chicago_auth_race'),
        chicago.hyphenated_identity.alias('chicago_auth_hyphenated_identity'),
        chicago.immigrant.alias('chicago_auth_immigrant'),
        chicago.sexual_identity.alias('chicago_auth_sexual_identity'),
        chicago.education.alias('chicago_auth_education'),
        chicago.mfa.alias('chicago_auth_mfa'),
        chicago.secondary_occupation.alias('chicago_auth_secondary_occupation'),
        chicago.coterie.alias('chicago_auth_coterie'),
        chicago.religion.alias('chicago_auth_religion'),
        chicago.ses.alias('chicago_auth_ses'),
        chicago.geography.alias('chicago_auth_geography'),
        chicago.text,
    )

    rdd = sc.union([gale_unified.rdd, chicago_unified.rdd])

    rdd = rdd.map(Novel.from_rdd)

    novels = spark.createDataFrame(rdd, Novel.schema)

    novels.write.mode('overwrite').parquet(dest)


if __name__ == '__main__':
    main()
