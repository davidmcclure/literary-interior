

import time

from lint.conn import sc


def work(i):
    time.sleep(1)
    return i+1


def main():
    data = sc.parallelize(range(100))
    result = data.map(work).collect()
    print(result)


if __name__ == '__main__':
    main()
