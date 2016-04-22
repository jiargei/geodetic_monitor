from common.constants import FACE_ONE
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

    def __init__(self, *args, **kwargs):
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

    def __init__(self, *args, **kwargs):
        """

        :param status:
        :param description:
        :param horizontal_angle:
        :param vertical_angle:
        :return:
        """
        super(AngleResponse, self).__init__(*args, **kwargs)
        hz = kwargs.get("horizontal_angle")
        v = kwargs.get("vertical_angle")
        self.horizontal_angle = float(format(hz, '.5f'))
        self.vertical_angle = float(format(v, '.5f'))


class DistanceResponse(Response):
    """

    """
    def __init__(self, slope_distance, *args, **kwargs):
        """

        :param slope_distance:
        :param status:
        :param description:
        :return:
        """
        super(DistanceResponse, self).__init__(*args, **kwargs)
        self.slope_distance = float(format(slope_distance, '.3f'))


class TemperatureResponse(Response):
    """

    """
    def __init__(self, *args, **kwargs):
        """

        :param temperature:
        :param status:
        :param description:
        :return:
        """
        super(TemperatureResponse, self).__init__(*args, **kwargs)
        t = kwargs.get("temperature")
        self.temperature = float(format(t, '.1f'))


class StringResponse(Response):
    """

    """
    def __init__(self, *args, **kwargs):
        """

        :param string:
        :param status:
        :param description:
        :return:
        """
        super(StringResponse, self).__init__(*args, **kwargs)
        s = kwargs.get("string")
        self.string = str(s)


class StateResponse(Response):
    """

    """
    def __init__(self, *args, **kwargs):
        super(StateResponse, self).__init__(*args, **kwargs)
        self.state = kwargs.get("state")


class FloatResponse(Response):
    """

    """
    def __init__(self, *args, **kwargs):
        super(FloatResponse, self).__init__(*args, **kwargs)
        v = kwargs.get("value")
        self.value = float(format(v, '.4f'))


class CoordinateResponse(Response):
    """

    """
    def __init__(self, *args, **kwargs):
        """

        :param easting:
        :param northing:
        :param height:
        :param status:
        :param description:
        :return:
        """
        super(CoordinateResponse, self).__init__(*args, **kwargs)
        e = kwargs.get("easting")
        n = kwargs.get("northing")
        h = kwargs.get("height")
        self.easting = float(format(e, '.4f'))
        self.northing = float(format(n, '.4f'))
        self.height = float(format(h, '.4f'))


class CompensatorResponse(Response):
    """

    """
    def __init__(self, *args, **kwargs):
        """

        :param compensator_cross:
        :param compensator_length:
        :param status:
        :param description:
        :return:
        """
        super(CompensatorResponse, self).__init__(*args, **kwargs)
        cc = kwargs.get("compensator_cross")
        cl = kwargs.get("compensator_length")
        self.compensator_cross = float(format(cc, '.5f'))
        self.compensator_length = float(format(cl, '.5f'))


class StationResponse(CoordinateResponse):
    """

    """
    def __init__(self, *args, **kwargs):
        super(StationResponse, self).__init__(*args, **kwargs)
        ih = kwargs.get("instrument_height", 0.0)
        self.instrument_height = float(format(ih, '.3f'))


class TachyMeasurementResponse(AngleResponse, DistanceResponse, TemperatureResponse):
    """

    """
    def __init__(self, *args, **kwargs):
        super(TachyMeasurementResponse, self).__init__(*args, **kwargs)
        self.reflector_height = float(kwargs.get("reflector_height", 0.0))
        self.face = int(kwargs.get("face", FACE_ONE))
        self.ppm = float(kwargs.get("ppm"))
        self.prism_constant = float(kwargs.get("prism_constant"))
        self.slope_distance_reduced = self.slope_distance  # TODO
