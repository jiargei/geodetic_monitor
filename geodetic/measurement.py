from point import Point
from calculations import polar


class TachyMeasurement(object):
    """

    """
    def __init__(self, horizontal_angle, vertical_angle, slope_distance, target_height):
        """

        Args:
            horizontal_angle:
            vertical_angle:
            slope_distance:

        Returns:

        """
        self.horizontal_angle = horizontal_angle
        self.vertical_angle = vertical_angle
        self.slope_distance = slope_distance
        self.target_height = target_height

    def to_grid(self):
        """

        Args:
            station:

        Returns: Point

        """
        return polar.polar_to_grid(Point(), self.horizontal_angle, self.vertical_angle, self.slope_distance)
