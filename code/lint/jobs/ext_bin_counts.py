

import numpy as np
import click

from lint.utils import get_spark
from lint.udf import _ext_bin_counts


@click.command()
@click.argument('src', type=click.Path())
@click.argument('dest', type=click.Path())
@click.argument('vocab', nargs=-1)
@click.option('--bin_count', type=int, default=20)
@click.option('--partitions', type=int, default=10)
def main(src, dest, vocab, bin_count, partitions):
    """Extract per-text bin counts.
    """
    sc, spark = get_spark()

    novels = spark.read.parquet(src)

    # Remove un-cleaned Chicago texts.
    novels = novels.filter(
        (novels.chicago_clean == True) |
        novels.chicago_clean.isNull()
    )

    ext_bin_counts = _ext_bin_counts(vocab, bin_count)

    counts = ext_bin_counts(novels.text.tokens.text).alias('counts')

    # Metadata + tokens.
    novels = novels.select(
        novels.corpus,
        novels.identifier,
        novels.title,
        novels.author_last,
        novels.author_first,
        novels.pub_year,
        counts,
    )

    novels = novels.repartition(partitions)

    writer = (novels.write
        .option('compression', 'bzip2')
        .mode('overwrite'))

    writer.json(dest)


if __name__ == '__main__':
    main()
