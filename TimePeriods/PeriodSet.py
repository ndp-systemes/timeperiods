from .Period import TimePeriod


class TimePeriodSet:
    """ An iterable containing one or more TimePeriod

    :param periods: One or more TimePeriod
    """

    def __init__(self, *periods):
        self._periods = []
        for period in periods:
            self += period

    @property
    def periods(self):
        """ All TimePeriod contained in this TimePeriodSet """
        return self._periods

    def __copy__(self):
        """ Makes a deep copy of a TimePeriodSet, copying all TimePeriod contained """
        new = self.__class__()
        new._periods = [period.copy() for period in self._periods]
        return new

    copy = __copy__

    def __ior__(self, other):
        """ Union of self and other

        :param other: If it is a TimePeriod, it will be added to the current set
                      If it is a TimePeriodSet, all of its TimePeriod will be added to the current set
        :rtype: TimePeriodSet
        """
        if isinstance(other, self.__class__):
            for period in other:
                self += period
            return self

        # Here we should have other as a Period
        intersection_periods = []
        begin_idx, end_idx = None, None

        for idx, period in enumerate(self):
            if begin_idx is None and period.end >= other.begin:
                begin_idx = idx

            if begin_idx is not None:
                if period.begin <= other.end:
                    # Here, period is at least partially included in other
                    intersection_periods.append(period)
                else:
                    # Here, period starts after other
                    end_idx = idx
                    break

        # If no common TimePeriod, new_period is exactly other.
        # Else, it starts with the earliest start, and ends with the latest end
        new_period = TimePeriod(
                    min(intersection_periods[0].begin, other.begin),
                    max(intersection_periods[-1].end, other.end)
                ) \
            if intersection_periods \
            else other

        self._periods = self._periods[:begin_idx] + \
            [new_period] + \
            (self._periods[end_idx:] if end_idx is not None else [])
        return self

    __iadd__ = __ior__

    def __iand__(self, other):
        """ Intersection of self and other

        :param other: A TimePeriod or TimePeriodSet; the current set will be equal to all the TimePeriod contained both
                      in itself and in other
        :rtype: TimePeriodSet
        """
        def _get_next_period(idx):
            idx += 1
            if idx >= len(self):
                return None, idx
            return self[idx], idx

        if not isinstance(other, self.__class__):
            other = (other,)

        idx = 0
        common_periods = []
        for other_period in other:
            if idx >= len(self):
                break

            period = self[idx]

            while period.end < other_period.begin:
                period, idx = _get_next_period(idx)
                if period is None:
                    break

            if period is None:
                break

            # Here we should have period.end >= other_period.begin
            while period.begin <= other_period.end:
                # Here, we have period.begin <= other_period.end and period.end >= other_period.begin
                common_periods.append(other_period & period)
                period, idx = _get_next_period(idx)
                if period is None:
                    break

            # Here, we have period.begin > other_period.end
            # We'll switch to the next period, but first, we need to "rewind" one period, because it may intersect
            # both the current other_period and the next
            if idx:
                idx -= 1

        self._periods = common_periods
        return self

    def __and__(self, other):
        """ Intersection between one or many TimePeriods

        :param other: a TimePeriodSet or TimePeriod
        :return: All TimePeriod contained both in self's `period` and in other
        """
        new = self.copy()
        new &= other
        return new

    def __or__(self, other):
        """ Union between one or manyTimePeriods

        :param other: a TimePeriodSet or TimePeriod
        :return: All TimePeriod contained either in self's `period` or in other
        """
        new = self.copy()
        new |= other
        return new

    __add__ = __or__

    def __len__(self):
        """ Return how many distinct TimePeriod are contained in this set """
        return len(self._periods)

    def __getitem__(self, item):
        """ Return the period at index `item` """
        return self._periods[item]

    def __iter__(self):
        for period in self._periods:
            yield period

    def __eq__(self, other):
        """ Checks if each of two TimePeriodSets' TimePeriods are identical """
        return len(self) == len(other) and all(period == other_period for period, other_period in zip(self, other))

    def __nonzero__(self):
        return bool(self._periods)

    def __repr__(self):
        return u"<TimePeriodSet(%s)>" % u", ".join(u"[%s, %s]" % (p.begin, p.end) for p in self)
