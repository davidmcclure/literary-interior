

from mpi4py import MPI

from lint import config
from lint.utils import mem_pct, enum
from lint.offset_cache import OffsetCache
from lint.corpus import Corpus
from lint.volume import Volume


Tags = enum('READY', 'WORK', 'RESULT', 'EXIT')


class DumpOffsets:


    def __init__(self):

        """
        Initialize the offset cache.
        """

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

            path_groups = corpus.path_groups(config['group_size'])

            closed_ranks = 0

            processed_groups = 0

            while closed_ranks < size-1:

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

                # ------
                # RESULT
                # ------
                elif tag == Tags.RESULT:
                    processed_groups += 1
                    print(processed_groups * config['group_size'], 'paths')

                # ----
                # EXIT
                # ----
                elif tag == Tags.EXIT:
                    closed_ranks += 1

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
                    comm.send(None, dest=0, tag=Tags.RESULT)

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

                vol = Volume.from_path(path)

                # Ignore non-English vols.
                if not vol.is_english:
                    continue

                # Get the token offset counts.
                offsets = vol.token_offsets(config['offset_resolution'])

                # Merge counts into the cache.
                self.cache.increment(vol.year, offsets)

                # Flush the cache to disk.
                if mem_pct() > config['max_mem_pct']:
                    self.flush()

            except Exception as e:
                print(e)


    def flush(self):

        """
        Flush the offset cache to disk.
        """

        self.cache.flush(config['result_dir'])
