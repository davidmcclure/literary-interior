

import time

from lint.utils import get_spark


def work(i):
    time.sleep(1)
    return i+1


def main():
    sc, _ = get_spark()
    data = sc.parallelize(range(100))
    result = data.map(work).collect()
    print(result)


if __name__ == '__main__':
    main()
