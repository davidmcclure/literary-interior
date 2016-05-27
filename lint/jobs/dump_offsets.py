

from mpi4py import MPI

from lint import config
from lint.utils import mem_pct, enum
from lint.offset_cache import OffsetCache
from lint.corpus import Corpus
from lint.volume import Volume


Tags = enum('READY', 'WORK', 'EXIT')


class DumpOffsets:


    def __init__(self, group_size=1000, max_mem_pct=80):

        """
        Set options, initialize the cache.

        Args:
            group_size (int)
            max_mem_pct (int)
        """

        self.group_size = group_size

        self.max_mem_pct = max_mem_pct

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
                    self.process(paths)

                # ----
                # EXIT
                # ----
                elif tag == Tags.EXIT:
                    break

            # Flush remaining counts.
            self.flush()

            # Notify exit.
            comm.send(None, dest=0, tag=Tags.EXIT)


    def process(self, paths):

        """
        Accumulate offset counts for a groups of paths

        Args:
            paths (list)
        """

        for path in paths:

            try:

                vol = Volume.from_path()

                # Ignore non-English vols.
                if not vol.is_english:
                    continue

                # Merge the offset counts.
                self.cache.increment(vol.year, vol.token_offsets())

                # Flush the cache to disk.
                if mem_pct() > self.max_mem_pct:
                    self.flush()

            except Exception as e:
                print(e)


    def flush(self):

        """
        Flush the offset cache to disk.
        """

        self.cache.flush(config['results'])
