

from mpi4py import MPI

from lint.offset_cache import OffsetCache
from lint.corpus import Corpus
from lint.volume import Volume


Tags = enum('READY', 'WORK', 'EXIT')


class IndexCount:


    def __init__(self, out_path, group_size=1000):

        """
        Set options, initialize the cache.

        Args:
            out_path (str)
            group_size (int)
        """

        self.out_path = out_path

        self.group_size = group_size

        self.cache = OffsetCache()


    def run(self):

        """
        Extract {year -> token -> offset -> count} for all volumes.
        """

        comm = MPI.COMM_WORLD

        size = comm.Get_size()
        rank = comm.Get_rank()

        status = MPI.Status()

        if rank == 0:

            corpus = Corpus.from_env()

            path_groups = corpus.path_groups(self.group_size)

            closed = 0
            while closed < size-1:

                # Get a work request from a rank.
                data = comm.recv(
                    status=status,
                    source=MPI.ANY_SOURCE,
                    tag=MPI.ANY_TAG,
                )

                source = status.Get_source()
                tag = status.Get_tag()

                # -----
                # READY
                # -----
                if tag == Tags.READY:

                    # Try to send a new group of paths.
                    try:
                        paths = next(path_groups)
                        comm.send(list(paths), dest=source, tag=Tags.WORK)

                    # If finished, close the rank.
                    except StopIteration:
                        comm.send(None, dest=source, tag=Tags.EXIT)

                # ----
                # EXIT
                # ----
                elif tag == Tags.EXIT:
                    closed += 1

        else:

            while True:

                # Ready for work.
                comm.send(None, dest=0, tag=Tags.READY)

                # Request paths.
                paths = comm.recv(
                    source=0,
                    tag=MPI.ANY_TAG,
                    status=status,
                )

                tag = status.Get_tag()

                # ----
                # WORK
                # ----
                if tag == Tags.WORK:
                    # TODO: extract offsets, flush when over N% memory
                    pass

                # ----
                # EXIT
                # ----
                elif tag == Tags.EXIT:
                    break

            # TODO: flush remaining counts

            # Notify exit.
            comm.send(None, dest=0, tag=Tags.EXIT)


    def process_paths(self, paths):

        """
        Accumulate offset counts for a groups of paths

        Args:
            paths (list)
        """

        for path in paths:

            try:

                vol = Volume.from_path()

                # TODO: merge offsets

            except Exception as e:
                print(e)
