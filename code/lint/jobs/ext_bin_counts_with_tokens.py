

import numpy as np
import click

from pyspark.sql.functions import size

from lint.utils import get_spark, read_vocab_file
from lint.udf import _ext_bin_counts


@click.command()
@click.argument('novels_src', type=click.Path())
@click.argument('vocab_path', type=click.Path())
@click.argument('dest', type=click.Path())
@click.option('--bin_count', type=int, default=4)
@click.option('--novel_partitions', type=int, default=10000)
@click.option('--out_partitions', type=int, default=100)
def main(novels_src, vocab_path, dest, bin_count,
    novel_partitions, out_partitions):
    """Extract per-text bin counts.
    """
    sc, spark = get_spark()

    novels = spark.read.parquet(novels_src)

    novels.repartition(novel_partitions)

    vocab = read_vocab_file(vocab_path)

    # Remove un-cleaned Chicago texts.
    novels = novels.filter(
        (novels.chicago_clean == True) |
        novels.chicago_clean.isNull()
    )

    ext_bin_counts = _ext_bin_counts(vocab, bin_count)

    counts = ext_bin_counts(novels.text.tokens.text)

    novels = (novels
        .withColumn('counts', counts)
        .withColumn('tokens', novels.text.tokens.text)
        .withColumn('tags', novels.text.tokens.tag)
        .drop(novels.text))

    novels = novels.repartition(out_partitions)

    writer = (novels.write
        .option('compression', 'bzip2')
        .mode('overwrite'))

    writer.json(dest)


if __name__ == '__main__':
    main()
