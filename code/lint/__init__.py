

import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    datefmt='%y/%m/%d %H:%M:%S',
)


log = logging.getLogger('lint')
