#!/usr/bin/env python


import json
import math

from lint.singletons import config
from lint.htrc.volume import Volume
from lint.offset_cache import OffsetCache
from lint.htrc.manifest  import Manifest
from lint.utils import mem_pct, round_to_decade


def dump_offsets():

    """
    Index year -> token -> offset -> count.
    """

    from mpi4py import MPI

    comm = MPI.COMM_WORLD

    size = comm.Get_size()
    rank = comm.Get_rank()

    # ** Scatter JSON-encoded segments.

    segments = None

    if rank == 0:
        manifest = Manifest.from_env()
        segments = manifest.json_segments(size)


    segment = comm.scatter(segments, root=0)

    # ** Gather offsets in segment.

    paths = json.loads(segment)

    print(rank, len(paths))

    cache = OffsetCache()

    for i, path in enumerate(paths):

        try:

            vol = Volume.from_path(path)

            # Ignore non-English vols.
            if not vol.is_english:
                continue

            # Get the token offset counts.
            offsets = vol.token_offsets(config['offset_resolution'])

            # Round to nearest decade.
            year = round_to_decade(vol.year)

            # Merge counts into cache.
            cache.increment(year, offsets)

        except Exception as e:
            print(e)

        if i%1000 == 0:
            print(rank, i, mem_pct())

    # Pickle to disk.
    cache.flush(config['result_dir'])


if __name__ == '__main__':
    dump_offsets()
