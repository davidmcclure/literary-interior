

import click

from lint import fs, paths
from lint.utils import try_or_none
from lint.conn import spark, sc
from lint.sources import GaleNovelXML
from lint.models import GaleNovel


@try_or_none
def parse_xml(path):
    return GaleNovelXML.read(path).row()


@click.command()
@click.option('--src', default=paths.GALE_SRC)
@click.option('--dest', default=paths.GALE_DEST)
def main(src, dest):
    """Ingest Gale.
    """
    paths = list(fs.scan(src, '\.xml'))

    paths = sc.parallelize(paths, len(paths))

    df = paths.map(parse_xml).filter(bool).toDF(GaleNovel.schema)

    df.write.mode('overwrite').parquet(dest)


if __name__ == '__main__':
    main()
