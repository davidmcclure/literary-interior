

import click

from lint import paths
from lint.utils import read_csv, try_or_none
from lint.conn import spark, sc
from lint.sources import ChicagoNovelMetadata
from lint.models import ChicagoNovel


@try_or_none
def parse_row(row, text_dir):
    return ChicagoNovelMetadata(row, text_dir).row()


@click.command()
@click.option('--csv_path', default=paths.CHICAGO_CSV_PATH)
@click.option('--text_dir', default=paths.CHICAGO_TEXT_DIR)
@click.option('--dest', default=paths.CHICAGO_DEST)
def main(csv_path, text_dir, dest):
    """Ingest Chicago novels.
    """
    rows = sc.parallelize(read_csv(csv_path))

    df = (rows
        .map(lambda r: parse_row(r, text_dir))
        .filter(bool)
        .toDF(ChicagoNovel.schema))

    df.write.mode('overwrite').parquet(dest)


if __name__ == '__main__':
    main()
