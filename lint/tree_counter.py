

import pprint

from functools import reduce

from lint.utils import flatten_dict


class TreeCounter:

    def __init__(self):

        """
        Initialize the count tree.
        """

        self.tree = {}

    def __repr__(self):

        """
        Print the tree.

        Returns: str
        """

        return pprint.pformat(self.tree, indent=2)

    def __setitem__(self, path, val):

        """
        Set the count for a path.
        """

        # TODO - test that sets with super/subsets of the path override.

        if not isinstance(path, tuple):
            path = (path,)

        def vivify(tree, key):

            i, key = key

            # If we're at the end of the path, set the value.
            if i == len(path)-1:
                tree[key] = val

            # If we're mid-path.
            elif type(tree.get(key)) is not dict:
                tree[key] = dict()

            return tree[key]

        reduce(vivify, enumerate(path), self.tree)

    def __getitem__(self, path):

        """
        Get the count for a path.
        """

        # TODO - test get a subset / superset path of existing path.

        if not isinstance(path, tuple):
            path = (path,)

        def vivify(tree, key):

            i, key = key

            if i == len(path)-1:
                return tree.get(key, 0)

            else:
                val = tree.get(key)
                return val if type(val) is dict else dict()

        return reduce(vivify, enumerate(path), self.tree)

    def flatten(self):

        """
        Generate flattened tuples of for all branches.

        Yields: (path1, path2, ..., count)
        """

        yield from flatten_dict(self.tree)
