#!/usr/bin/env python


from lint.singletons import config, session
from lint.models import Offset
from lint.offset_cache import OffsetCache


if __name__ == '__main__':

    # Merge the pickled MPI results.
    results = OffsetCache.from_results(config['results']['htrc'])

    # Flush to SQLite.
    Offset.flush('htrc', results)

    session.commit()
