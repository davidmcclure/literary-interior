

import click

from lint import fs
from lint.conn import spark, sc
from lint.sources import GaleNovelXML
from lint.models import GaleNovel


def parse_xml(path):
    return GaleNovelXML.read(path).row()


@click.command()
@click.option('--src', default='/data/gale')
@click.option('--dest', default='/data/gale.parquet')
def main(src, dest):
    """Ingest Gale.
    """
    paths = list(fs.scan(src, '\.xml'))

    paths = sc.parallelize(paths, len(paths))

    df = paths.map(parse_xml).toDF(GaleNovel.schema)

    df.write.mode('overwrite').parquet(dest)


if __name__ == '__main__':
    main()
