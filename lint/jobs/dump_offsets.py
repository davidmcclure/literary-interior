

import json

from lint.offset_cache import OffsetCache
from lint.utils import mem_pct


class DumpOffsets:

    def segments(self, size):
        raise NotImplementedError

    def increment(self, arg):
        raise NotImplementedError

    def flush(self, arg):
        raise NotImplementedError

    def __call__(self):

        """
        Dump year -> token -> offset -> count.
        """

        from mpi4py import MPI

        comm = MPI.COMM_WORLD

        size = comm.Get_size()
        rank = comm.Get_rank()

        # ** Scatter JSON-encoded segments.

        segments = None

        if rank == 0:
            segments = self.segments(size)

        segment = comm.scatter(segments, root=0)

        args = json.loads(segment)

        print(rank, len(args))

        ## ** Gather offsets, flush.

        self.cache = OffsetCache()

        for i, arg in enumerate(args):

            try:
                self.increment(arg)

            except Exception as e:
                print(e)

            if i%1000 == 0:
                print(rank, i, mem_pct())

        self.flush()
