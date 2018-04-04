

import numpy as np
import click

from pyspark.sql.functions import udf, size
from pyspark.sql import types as T

from lint.utils import get_spark, zip_bin


@udf(T.FloatType())
def avg_len(tokens):
    return float(np.mean([len(t) for t in tokens]))


@click.command()
@click.argument('src', type=click.Path())
@click.argument('dest', type=click.Path())
def main(src, dest):
    """Extract per-text bin counts.
    """
    sc, spark = get_spark()

    novels = spark.read.parquet(src)

    novels = novels.select(
        novels.corpus,
        novels.identifier,
        novels.title,
        novels.author_last,
        novels.author_first,
        novels.pub_year,
        avg_len(novels.text.tokens.text).alias('avg_word_len'),
        size(novels.text.tokens.text).alias('word_count')
    )

    novels = novels.repartition(1)

    novels.write.mode('overwrite').json(dest)


if __name__ == '__main__':
    main()
