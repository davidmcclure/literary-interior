

import click

from lint.utils import get_spark
from lint.sources import ChicagoAuthorCSVRow
from lint.models import ChicagoAuthor


@click.command()
@click.argument('src', type=click.Path())
@click.argument('dest', type=click.Path())
def main(src, dest):
    """Ingest Chicago authors.
    """
    _, spark = get_spark()

    rows = list(ChicagoAuthorCSVRow.read_csv(src))

    df = spark.createDataFrame(rows, ChicagoAuthor.schema)

    df.write.mode('overwrite').parquet(dest)


if __name__ == '__main__':
    main()
