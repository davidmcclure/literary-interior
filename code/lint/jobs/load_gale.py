

import click

from lint import fs
from lint.utils import try_or_none
from lint.conn import spark, sc
from lint.sources import GaleNovelXML
from lint.models import GaleNovel


@try_or_none
def parse_xml(path):
    return GaleNovelXML.read(path).row()


@click.command()
@click.argument('src', type=click.Path())
@click.argument('dest', type=click.Path())
def main(src, dest):
    """Ingest Gale.
    """
    paths = list(fs.scan(src, '\.xml'))

    paths = sc.parallelize(paths, len(paths))

    df = paths.map(parse_xml).toDF(GaleNovel.schema)

    df.write.mode('overwrite').parquet(dest)


if __name__ == '__main__':
    main()
