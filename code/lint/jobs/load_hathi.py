

import click

import  pandas as pd

from lint.utils import try_or_none, get_spark
from lint.models import HathiVolume


@try_or_none
def parse_vol(genre_row, vol_root):
    pass


@click.command()
@click.argument('genre_src', type=click.Path())
@click.argument('vol_root', type=click.Path())
@click.argument('dest', type=click.Path())
def main(genre_src, vol_root, dest):
    """Ingest Gale.
    """
    sc, spark = get_spark()

    genres = spark.read.json(genre_src)

    df = (genres.rdd
        .map(lambda row: parse_vol(row, vol_root))
        .filter(bool)
        .toDF(HathiVolume.schema))

    df.write.mode('overwrite').parquet(dest)

    print(genres.collect())


if __name__ == '__main__':
    main()
