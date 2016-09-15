

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

        Args:
            path (tuple)
            val (int)
        """

        if not isinstance(path, tuple):
            path = (path,)

        def vivify(tree, level):

            i, key = level

            # If we're at the end of the path, set the value.
            if i == len(path)-1:
                tree[key] = val

            # Otherwise, if no existing subtree, add one.
            elif type(tree.get(key)) is not dict:
                tree[key] = dict()

            return tree[key]

        reduce(vivify, enumerate(path), self.tree)

    def __getitem__(self, path):

        """
        Get the count for a path.

        Args:
            path (tuple)
        """

        if not isinstance(path, tuple):
            path = (path,)

        def vivify(tree, level):

            i, key = level

            val = tree.get(key)

            # If we're at the end of the path, return the value.
            if i == len(path)-1:
                return val if type(val) is int else 0

            # Otherwise return the next sub-tree.
            else:
                return val if type(val) is dict else dict()

        return reduce(vivify, enumerate(path), self.tree)

    def flatten(self):

        """
        Generate flattened tuples of for all branches.

        Yields: (path1, path2, ..., count)
        """

        yield from flatten_dict(self.tree)
