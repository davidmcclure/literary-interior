

import numpy as np
import click

from lint.utils import get_spark, read_vocab_file
from lint.udf import _ext_bin_counts


@click.command()
@click.argument('vols_src', type=click.Path())
@click.argument('vocab_path', type=click.Path())
@click.argument('dest', type=click.Path())
@click.option('--bin_count', type=int, default=20)
@click.option('--partitions', type=int, default=10)
def main(vols_src, vocab_path, dest, bin_count, partitions):
    """Extract per-text bin counts.
    """
    sc, spark = get_spark()

    vols = spark.read.parquet(vols_src)

    vocab = read_vocab_file(vocab_path)

    ext_bin_counts = _ext_bin_counts(vocab, bin_count)

    counts = ext_bin_counts(vols.tokens.text)

    # Select counts, drop text.
    vols = vols.withColumn('counts', counts).drop(vols.tokens)

    vols = vols.repartition(partitions)

    writer = (vols.write
        .option('compression', 'bzip2')
        .mode('overwrite'))

    writer.json(dest)


if __name__ == '__main__':
    main()
