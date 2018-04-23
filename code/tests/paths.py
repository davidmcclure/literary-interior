

import os


FIXTURES_ROOT = os.path.join(os.path.dirname(__file__), 'fixtures')

GALE_SRC = os.path.join(FIXTURES_ROOT, 'gale')
GALE_DEST = '/tmp/gale.parquet'

CHICAGO_NOVELS_CSV_PATH = os.path.join(FIXTURES_ROOT, 'chicago/CHICAGO_NOVEL_CORPUS_METADATA/CHICAGO_CORPUS_NOVELS.csv')
CHICAGO_TEXT_DIR = os.path.join(FIXTURES_ROOT, 'chicago/CHICAGO_NOVEL_CORPUS')
CHICAGO_NOVELS_DEST = '/tmp/chicago-novels.parquet'

NOVELS_DEST = '/tmp/novels.parquet'
