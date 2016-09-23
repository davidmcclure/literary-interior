

import numpy as np
import json

from lint.count_cache import CountCache
from lint.utils import mem_pct


class Extract:

    def args(self):
        raise NotImplementedError

    def add_volume(self, arg):
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

            segments = [
                json.dumps(list(s))
                for s in np.array_split(list(self.args()), size)
            ]

        segment = comm.scatter(segments, root=0)

        args = json.loads(segment)

        print(rank, len(args))

        ## ** Gather offsets, flush.

        self.cache = CountCache()

        for i, arg in enumerate(args):

            try:

                if type(arg) is dict:
                    self.add_volume(**arg)

                else:
                    self.add_volume(arg)

            except Exception as e:
                print(e)

            if i%100 == 0:
                print(rank, i, mem_pct())

        self.flush()
