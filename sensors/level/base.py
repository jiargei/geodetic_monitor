from sensors.base import Measurement


class TiltMeasurement(Measurement):
    """

    """
    def __init__(self, tilt_x, tilt_y, status, description):
        """

        :param compensator_cross:
        :param compensator_length:
        :param status:
        :param description:
        :return:
        """
        super(TiltMeasurement, self).__init__(status, description)
        self.tilt_x = tilt_x
        self.tilt_y = tilt_y
