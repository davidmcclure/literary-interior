

import time

from lint.conn import spark, sc
from lint.models import Text


def work(i):
    return Text.parse('Does this work?')


def main():
    data = sc.parallelize(range(100))
    result = data.map(work).collect()
    print(result)


if __name__ == '__main__':
    main()
