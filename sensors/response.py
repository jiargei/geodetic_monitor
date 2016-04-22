from sensors.tachy.base import FACE_ONE, FACE_TWO
from uuid import uuid1

from django.utils import timezone

RESPONSE_SUCCESS = 200
RESPONSE_WARN = 500
RESPONSE_FAIL = 400
RESPONSE_DESCRIPTION = "OK"


class Response(object):
    """
    Basic Response for no specific information output
    """

    VALUES = []

    def __init__(self, **kwargs):
        """

        :param status:
        :param description:
        :return:
        """
        self.uuid = kwargs.get("uuid", str(uuid1()))
        self.created = kwargs.get("created", timezone.localtime(timezone.now()))
        tmp_dict = kwargs.get("data_dict", {})
        if tmp_dict:
            self.status = tmp_dict["status"]
            self.description = tmp_dict["description"]
            for key in self.VALUES:
                if tmp_dict.has_key(key):
                    self.__setattr__(str(key).lower(), tmp_dict[key])
        else:
            self.status = kwargs.get("status", RESPONSE_SUCCESS)
            self.description = kwargs.get("description", RESPONSE_DESCRIPTION)


class DateResponse(Response):
    """

    """

    VALUES = ["DATE"]

    def __init__(self, **kwargs):
        super(DateResponse, self).__init__(**kwargs)
        self.date = kwargs.get("date")


class AngleResponse(Response):
    """

    """

    VALUES = ["HORIZONTAL_ANGLE", "VERTICAL_ANGLE"]

    def __init__(self, horizontal_angle, vertical_angle, **kwargs):
        """

        :param status:
        :param description:
        :param horizontal_angle:
        :param vertical_angle:
        :return:
        """
        super(AngleResponse, self).__init__(**kwargs)
        self.horizontal_angle = float(kwargs.get("horizontal_angle"))
        self.vertical_angle = float(kwargs.get("vertical_angle"))


class DistanceResponse(Response):
    """

    """
    def __init__(self, slope_distance, **kwargs):
        """

        :param slope_distance:
        :param status:
        :param description:
        :return:
        """
        super(DistanceResponse, self).__init__(**kwargs)
        self.slope_distance = float(slope_distance)


class TemperatureResponse(Response):
    """

    """
    def __init__(self, temperature, **kwargs):
        """

        :param temperature:
        :param status:
        :param description:
        :return:
        """
        super(TemperatureResponse, self).__init__(**kwargs)
        self.temperature = float(temperature)


class StringResponse(Response):
    """

    """
    def __init__(self, string, **kwargs):
        """

        :param string:
        :param status:
        :param description:
        :return:
        """
        super(StringResponse, self).__init__(**kwargs)
        self.string = str(string)


class StateResponse(Response):
    """

    """
    def __init__(self, state, **kwargs):
        super(StateResponse, self).__init__(**kwargs)
        self.state = state


class FloatResponse(Response):
    """

    """
    def __init__(self, value, **kwargs):
        super(FloatResponse, self).__init__(**kwargs)
        self.value = float(value)


class CoordinateResponse(Response):
    """

    """
    def __init__(self, easting, northing, height, **kwargs):
        """

        :param easting:
        :param northing:
        :param height:
        :param status:
        :param description:
        :return:
        """
        super(CoordinateResponse, self).__init__(**kwargs)
        self.easting = float(easting)
        self.northing = float(northing)
        self.height = float(height)


class CompensatorResponse(Response):
    """

    """
    def __init__(self, compensator_cross, compensator_length, **kwargs):
        """

        :param compensator_cross:
        :param compensator_length:
        :param status:
        :param description:
        :return:
        """
        super(CompensatorResponse, self).__init__(**kwargs)
        self.compensator_cross = float(compensator_cross)
        self.compensator_length = float(compensator_length)


class StationResponse(CoordinateResponse):
    """

    """
    def __init__(self, instrument_height=0., **kwargs):
        super(StationResponse, self).__init__(**kwargs)
        self.instrument_height = float(instrument_height)


class TachyMeasurementResponse(AngleResponse, DistanceResponse, TemperatureResponse, CompensatorResponse):
    """

    """
    def __init__(self, **kwargs):
        super(TachyMeasurementResponse).__init__(**kwargs)
        self.reflector_height = float(kwargs.get("reflector_height", 0.0))
        self.face = int(kwargs.get("face", FACE_ONE))
        self.ppm = float(kwargs.get("ppm"))
        self.prism_constant = float(kwargs.get("prism_constant"))
        self.slope_distance_reduced = self.slope_distance  # TODO
