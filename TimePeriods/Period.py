# coding=utf-8
from datetime import datetime


INFINITY_BEGIN = datetime.min
INFINITY_END = datetime.max


class InvalidPeriodException(Exception):
    """ Raised when a period is incoherent, ie with its beginning later than its end """
    def __init__(self, begin, end):
        self.start, self.end = begin, end

    def __str__(self):
        return u"A périod taking place between %s and %s cannot exist" % (self.begin, self.end)


class SeparatePeriodsExceptions(Exception):
    """ Raised when two periods or more should have an intersection, but have not """
    def __init__(self, *periods):
        self.periods = tuple(periods)

    def __str__(self):
        return u"The following period do not have a common intersection : %s" % u", ".join(self.periods)


class TimePeriod:
    """ An immutable object describing a time period, with a beginning and an end

    :param begin: datetime marking the beginning of the period or None if infinite
    :param end: datetime marking the beginning of the period, taking place AFTER begin or None if infinite
    """

    __slots__ = []

    def __init__(self, begin, end):
        if begin is None:
            begin = INFINITY_BEGIN
        if end is None:
            end = INFINITY_END
        if begin >= end:
            raise InvalidPeriodException(begin, end)
        self.begin = begin
        self.end = end

    @property
    def duration(self):
        return self.end - self.begin

    def __copy__(self):
        return self.__class__(self.begin, self.end)

    def copy(self):
        return self.__copy__()

    def __str__(self):
        return u"%s - %s" % (self.begin, self.end)

    def __repr__(self):
        return u"<TimePeriod(%s, %s)>" % (self.begin, self.end)

    def __gt__(self, other):
        """ Compare if this period starts after another """
        return self.begin > other.begin

    def __lt__(self, other):
        """ Compare if this period starts before another """
        return self.begin < other.begin

    def __eq__(self, other):
        """ Compare if this period starts and ends on the same dates as another """
        return self.begin == other.begin and self.end == other.end

    def __ge__(self, other):
        """ Compare if this period is equal or starts later than another """
        return self == other or self > other

    def __le__(self, other):
        """ Compare if this period is equal or starts earlier than another """
        return self == other or self < other

    def __contains__(self, item):
        """ Test if the item and this period overlap """
        if isinstance(item, self.__class__):
            return self.begin <= item.end and self.end >= item.begin
        return self.begin <= item <= self.end

    def __or__(self, other):
        """ Merge two periods into one

        If the two are disjointed, raise a SeparatePeriodsExceptions
        """
        first, second = sorted((self, other))
        if first.end < second.begin:
            raise SeparatePeriodsExceptions((first, second))
        if first.end >= second.end:
            return first
        else:
            return self.__class__(first.begin, second.end)

    def __and__(self, other):
        """ Makes the intersection between two periods

        If the two are disjointed, raise a SeparatePeriodsExceptions
        """
        first, second = sorted((self, other))
        if first.end < second.begin:
            raise SeparatePeriodsExceptions((first, second))
        if second.end <= first.end:
            return second
        else:
            return self.__class__(second.begin, first.end)

    __add__ = __or__
