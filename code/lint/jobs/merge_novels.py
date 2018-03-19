

import click

from pyspark.sql.functions import lit

from lint import paths
from lint.conn import spark, sc
from lint.models import Novel


@click.command()
@click.option('--gale_src', default=paths.GALE_DEST)
@click.option('--chicago_src', default=paths.CHICAGO_DEST)
@click.option('--dest', default=paths.NOVELS_DEST)
def main(gale_src, chicago_src, dest):
    """Ingest Gale.
    """
    gale = spark.read.parquet(gale_src)
    chicago = spark.read.parquet(chicago_src)

    gale_unified = gale.select(
        lit('gale').alias('corpus'),
        gale.psmid.alias('identifier'),
        gale.full_title.alias('title'),
        gale.author_last,
        gale.author_first,
        gale.pub_date_start.alias('pub_year'),
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
        chicago.clean.alias('chicago_clean'),
        chicago.text,
    )

    rdd = sc.union([gale_unified.rdd, chicago_unified.rdd])

    rdd = rdd.map(Novel.from_rdd)

    novels = spark.createDataFrame(rdd, Novel.schema)

    novels.write.mode('overwrite').parquet(dest)


if __name__ == '__main__':
    main()
