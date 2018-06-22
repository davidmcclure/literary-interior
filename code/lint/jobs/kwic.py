

import numpy as np
import click

from lint.utils import get_spark


@click.command()
@click.argument('src', type=click.Path())
@click.argument('kw', type=str)
@click.argument('dest', type=click.Path())
@click.option('--n', type=int, default=1000)
@click.option('--o1', type=float, default=0)
@click.option('--o2', type=float, default=1)
def main(src, kw, dest, n, o1, o2):
    """Get KWIC matches.
    """
    sc, spark = get_spark()

    novels = spark.read.parquet(novels_src)

    # Remove un-cleaned Chicago texts.
    novels = novels.filter(
        (novels.chicago_clean == True) |
        novels.chicago_clean.isNull()
    )


if __name__ == '__main__':
    main()
