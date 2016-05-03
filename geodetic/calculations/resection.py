from .. point import Point, MeasuredPoint
from adjustment.adjustment import Adjustment2D, Adjustment1D


class Resection(object):
    """

    """
    def __init__(self, **kwargs):
        """

        Args:
            **kwargs:

        Returns:

        """
        self.station = kwargs.get("station", Point())
        self.target_list = []
        self.__is_set = False

    def add_target(self, t):
        assert isinstance(t, MeasuredPoint)
        self.target_list.append(t)

    def can_calculate(self):
        """

        Returns:

        """
        return len(self.target_list) >= 2

    def calculate(self):

        assert self.can_calculate()
        a2d = Adjustment2D()
        a1d = Adjustment1D()

        for ti in self.target_list:
            a2d.add_target(ti)
            a1d.add_target(ti)

        a2d.calculate()
        a1d.calculate()

        self.station = a2d.station + a1d.station
        self.__is_set = True
