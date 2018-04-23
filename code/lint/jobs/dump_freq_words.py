

import click

from lint.utils import get_spark


@click.command()
@click.argument('src', type=click.Path())
@click.argument('dest', type=click.Path())
@click.argument('n', type=int)
def main(src, dest, n):
    """Dump list of N most frequent words.
    """
    sc, spark = get_spark()

    novels = spark.read.parquet(src)

    novels = novels.select(novels.text.tokens.text.alias('tokens'))

    counts = (novels.rdd
        .flatMap(lambda r: (t.lower() for t in r.tokens))
        .map(lambda t: (t, 1))
        .reduceByKey(lambda a, b: a + b)
        .takeOrdered(n, lambda x: -x[1]))

    with open(dest, 'w') as fh:
        for token, _ in counts:
            print(token, file=fh)


if __name__ == '__main__':
    main()
