

import click

from lint import fs
from lint.utils import read_csv
from lint.conn import spark, sc
from lint.models import ChicagoNovel


def parse_row(row, text_dir):
    return ChicagoNovelMetadata(row, text_dir).row()


@click.command()
@click.argument('csv_path', type=click.Path())
@click.argument('text_dir', type=click.Path())
@click.argument('dest', type=click.Path())
def main(csv, text_dir, dest):
    """Ingest Chicago novels.
    """
    rows = sc.parallelize(read_csv(csv_path))

    df = (rows
        .map(lambda r: parse_row(r, text_dir))
        .toDF(ChicagoNovel.schema))

    df.write.model('parquet').parquet(dest)


if __name__ == '__main__':
    main()
