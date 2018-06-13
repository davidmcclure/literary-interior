

import click

from pyspark.sql import Row
from pyspark.sql.functions import rand

from lint.utils import get_spark, zip_offset


def w2v_sents(tokens):
    """Generate space-delimited sentences within an interval.
    """
    sents = {}

    for token, offset in zip_offset(tokens):

        offset_str = '%.4f' % offset

        # Offset before first token.
        if token.sent_i not in sents:
            sents[token.sent_i] = [offset_str, token.text]

        else:
            sents[token.sent_i].append(token.text)

    for sent_i in sorted(sents.keys()):
        yield Row(sent=' '.join(sents[sent_i]))


@click.command()
@click.argument('src', type=click.Path())
@click.argument('dest', type=click.Path())
@click.option('--partitions', type=int, default=100)
def main(src, dest, partitions):
    """Dump space-delimited sentences for word2vec.
    """
    sc, spark = get_spark()

    novels = spark.read.parquet(src)

    # Just clean Chicago, for now.
    novels = novels.filter(novels.chicago_clean==True)

    tokens = novels.select(novels.text.tokens.alias('tokens'))

    sents = (tokens.rdd
        .flatMap(lambda t: w2v_sents(t.tokens))
        .toDF())

    # Random shuffle.
    sents = sents.orderBy(rand())

    sents.repartition(partitions).write.mode('overwrite').text(dest)


if __name__ == '__main__':
    main()
