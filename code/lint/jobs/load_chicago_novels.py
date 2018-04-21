

import click

from lint.sources import ChicagoNovelMetadata
from lint.models import ChicagoNovel
from lint.utils import read_csv, try_or_none, get_spark


@try_or_none
def parse_row(row, text_dir):
    return ChicagoNovelMetadata(row, text_dir).row()


@click.command()
@click.argument('csv_path', type=click.Path())
@click.argument('text_dir', type=click.Path())
@click.argument('dest', type=click.Path())
def main(csv_path, text_dir, dest):
    """Ingest Chicago novels.
    """
    sc, _ = get_spark()

    rows = list(read_csv(csv_path))

    rows = sc.parallelize(rows, len(rows))

    df = (rows
        .map(lambda r: parse_row(r, text_dir))
        .filter(bool)
        .toDF(ChicagoNovel.schema))

    df.write.mode('overwrite').parquet(dest)


if __name__ == '__main__':
    main()
