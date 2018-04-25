

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
def main(src, dest):
    """Dump list of N most frequent words.
    """
    sc, spark = get_spark()

    novels = spark.read.parquet(src)

    tokens = novels.select(novels.text.tokens.alias('tokens'))

    sents = (tokens.rdd
        .flatMap(lambda t: w2v_sents(t.tokens, 0.95, 1))
        .toDF())

    sents.coalesce(10).write.mode('overwrite').text(dest)


if __name__ == '__main__':
    main()
