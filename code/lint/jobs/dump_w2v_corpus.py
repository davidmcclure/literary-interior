

import click

from collections import defaultdict

from pyspark.sql import Row

from lint.utils import get_spark, zip_offset


def w2v_sents(tokens, offset1, offset2):
    """Generate space-delimited sentences within an interval.
    """
    sents = defaultdict(list)

    for token, offset in zip_offset(tokens):
        if offset >= offset1 and offset <= offset2:
            sents[token.sent_i].append(token.text.lower())

    for sent_i in sorted(sents.keys()):
        yield Row(sent=' '.join(sents[sent_i]))


@click.command()
@click.argument('src', type=click.Path())
@click.argument('dest', type=click.Path())
@click.argument('offset1', type=float)
@click.argument('offset2', type=float)
@click.option('--partitions', type=int, default=100)
def main(src, dest, offset1, offset2, partitions):
    """Dump space-delimited sentences for word2vec.
    """
    sc, spark = get_spark()

    novels = spark.read.parquet(src)

    # Remove un-cleaned Chicago texts.
    novels = novels.filter(
        (novels.chicago_clean == True) |
        novels.chicago_clean.isNull()
    )

    tokens = novels.select(novels.text.tokens.alias('tokens'))

    sents = (tokens.rdd
        .flatMap(lambda t: w2v_sents(t.tokens, offset1, offset2))
        .toDF())

    sents.repartition(partitions).write.mode('overwrite').text(dest)


if __name__ == '__main__':
    main()
