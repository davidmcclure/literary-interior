

import click

from lint.utils import get_spark


@click.command()
@click.argument('src', type=click.Path())
@click.argument('dest', type=click.Path())
@click.option('--fraction', type=float, default=0.1)
@click.option('--seed', type=int, default=1)
@click.option('--partitions', type=int, default=500)
def main(src, dest, fraction, seed, partitions):
    """Sample novels, dump JSON.
    """
    sc, spark = get_spark()

    novels = spark.read.parquet(src)

    novels = novels.sample(False, fraction, seed).coalesce(partitions)

    novels.write.mode('overwrite').json(dest)


if __name__ == '__main__':
    main()
