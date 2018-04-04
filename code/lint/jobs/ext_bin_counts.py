

import numpy as np
import click

from pyspark.sql.functions import udf
from pyspark.sql import types as T

from lint.utils import get_spark, zip_bin


COUNT_SCHEMA = T.MapType(
    T.StringType(),
    T.ArrayType(T.IntegerType()),
)


def _ext_bin_counts(vocab, bin_count=20):
    """Count binned tokens.
    """
    vocab = set(vocab)

    @udf(COUNT_SCHEMA)
    def worker(tokens):

        # Downcase tokens.
        tokens = [t.lower() for t in tokens]

        counts = {
            token: [0] * bin_count
            for token in vocab
        }

        for token, bin in zip_bin(tokens, bin_count):
            if token in vocab:
                counts[token][bin] += 1

        return counts

    return worker


@click.command()
@click.argument('src', type=click.Path())
@click.argument('dest', type=click.Path())
@click.argument('vocab', nargs=-1)
@click.option('--partitions', type=int, default=10)
def main(src, dest, vocab, partitions):
    """Extract per-text bin counts.
    """
    sc, spark = get_spark()

    novels = spark.read.parquet(src)

    # Remove un-cleaned Chicago texts.
    novels = novels.filter(
        (novels.chicago_clean == True) |
        novels.chicago_clean.isNull()
    )

    ext_bin_counts = _ext_bin_counts(vocab)

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
