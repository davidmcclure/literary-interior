

import numpy as np
import click

from lint.utils import get_spark, read_vocab_file
from lint.udf import _ext_bin_counts


@click.command()
@click.argument('novels_src', type=click.Path())
@click.argument('vocab_path', type=click.Path())
@click.argument('dest', type=click.Path())
@click.option('--bin_count', type=int, default=20)
@click.option('--partitions', type=int, default=10)
def main(novels_src, vocab_path, dest, bin_count, partitions):
    """Extract per-text bin counts.
    """
    sc, spark = get_spark()

    novels = spark.read.parquet(novels_src)

    vocab = read_vocab_file(vocab_path)

    # Remove un-cleaned Chicago texts.
    novels = novels.filter(
        (novels.chicago_clean == True) |
        novels.chicago_clean.isNull()
    )

    ext_bin_counts = _ext_bin_counts(vocab, bin_count)

    counts = ext_bin_counts(novels.text.tokens.text)

    # Select counts, drop text.
    novels = novels.withColumn('counts', counts).drop(novels.text)

    novels = novels.repartition(partitions)

    writer = (novels.write
        .option('compression', 'bzip2')
        .mode('overwrite'))

    writer.json(dest)


if __name__ == '__main__':
    main()
