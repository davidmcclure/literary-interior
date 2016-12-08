# first line: 110
    @classmethod
    def token_counts(cls, min_count=0):

        """
        Get total (un-bucketed) token counts.

        Args:
            min_count (int)

        Returns: OrderedDict
        """

        query = (
            session
            .query(cls.token, func.sum(cls.count))
            .group_by(cls.token)
            .having(func.sum(cls.count) > min_count)
            .order_by(func.sum(cls.count).desc())
        )

        return OrderedDict(query.all())
