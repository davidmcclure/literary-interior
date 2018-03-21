

import click

from lint import fs
from lint.utils import try_or_none, get_spark
from lint.sources import GaleNovelXML
from lint.models import GaleNovel


@try_or_none
def parse_xml(path):
    return GaleNovelXML.read(path).row()


@click.command()
@click.option('--src', type=click.Path())
@click.option('--dest', type=click.Path())
def main(src, dest):
    """Ingest Gale.
    """
    sc, _ = get_spark()

    paths = list(fs.scan(src, '\.xml'))

    paths = sc.parallelize(paths, len(paths))

    df = (paths
        .map(parse_xml)
        .filter(bool)
        .toDF(GaleNovel.schema))

    df.write.mode('overwrite').parquet(dest)


if __name__ == '__main__':
    main()
