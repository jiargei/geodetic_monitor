# -*- coding: utf-8 -*-

# Third Party Module Import
import random

from serial import EIGHTBITS
from serial import PARITY_NONE
from serial import STOPBITS_ONE

# Package Import
from sensors.tachy.base import Tachy
from sensors.response import Response, TemperatureResponse, StringResponse, StateResponse, FloatResponse
from sensors.response import CompensatorResponse, CoordinateResponse, AngleResponse, StationResponse
from sensors.response import TachyMeasurementResponse, DistanceResponse
from geodetic.calculations import polar
from geodetic.point import Point
from common.constants import FACE_ONE, FACE_TWO, OFF

from django.utils import timezone
from sensors import base as b
from common.utils import generate


# Code


class FakeTachy(Tachy):
    """
    Produces allways same measurements with:

    Punkt          Epoche     Y  [m]      X  [m]         H  [m]   Code   MS
    DP01                      5195.093    337187.746    156.225          M34
    POS1                      5191.591    337195.883    156.168          M34

    HZ = 174.1248
    V = 99.5891
    SD = 8.859

    """

    brand = "FaKeBrAnD"
    model = "FaKeMoDeL"
    model_type = "Fake"
    sensor_type = "Fake"

    def __init__(self, *args, **kwargs):
        super(FakeTachy, self).__init__(*args, **kwargs)
        self.__horizontal_angle = 174.1248 + random.random()*3e-3
        self.__vertical_angle = 99.5891 + random.random()*3e-3
        self.__slope_distance = 8.859 + random.random() * 2e-3
        self.__connected = True
        self.__laser_pointer = OFF
        self.__face = FACE_ONE
        self.__compensator_cross = random.random()*1e-4
        self.__compensator_length = random.random()*1e-4
        self.__prism_constant = 0.0175
        self.__reflector_height = 0.0
        self.__instrument_height = 0.0
        self.__instrument_number = "95173"
        self.__instrument_name = "Fake Tachymeter v0.1"
        self.__station_easting = 5191.591
        self.__station_northing = 337195.883
        self.__station_height = 156.168
        p = polar.polar_to_grid(p1=Point(self.__station_easting,
                                         self.__station_northing,
                                         self.__station_height),
                                azimut=self.__horizontal_angle,
                                zenith=self.__vertical_angle,
                                distance=self.__slope_distance
                                )
        self.__easting = p.x
        self.__northing = p.y
        self.__height = p.z
        self.__orientation = 0.0
        self.__temperature = 21.14 + random.random()*1e-1
        self.__path = "/dev/null"
        self.__baudrate = 9600
        self.__bytesize = EIGHTBITS
        self.__stopbits = STOPBITS_ONE
        self.__parity = PARITY_NONE
        self.__time_out = 5
        self.__edm_mode = 1
        self.__atr_mode = 1
        self.__hz_tolerance = 0.0030
        self.__v_tolerance = 0.0030
        self.__level = 1

    def set_instrument_name(self, value):
        """
        NOT ALLOWED
        :param value:
        :return:
        """
        pass

    def set_instrument_number(self, value):
        """
        NOT ALLOWED
        :param value:
        :return:
        """
        pass

    def fine_adjust(self):
        return Response(description="Aiming at target")

    def get_compensator(self):
        m = CompensatorResponse(compensator_cross=self.__compensator_cross,
                                compensator_length=self.__compensator_length)
        return m

    def set_angles(self, hz, v, atr):
        """

        :param hz:
        :param v:
        :param atr:
        :return:
        """
        self.__horizontal_angle = hz
        self.__vertical_angle = v
        return Response()

    def get_angles(self, atr):
        """
        Liefert die Aktuellen Stellwinkel zurück
        :param atr:
        :return:
        """
        eps_hz = random.random()*4e-4 if atr else random.random() * 2e-3
        eps_v = random.random()*4e-4 if atr else random.random() * 2e-3
        return AngleResponse(horizontal_angle=self.__horizontal_angle+eps_hz,
                             vertical_angle=self.__vertical_angle+eps_v)

    def set_search_windows(self, search_horizontal, search_vertical):
        self.__hz_tolerance = search_horizontal
        self.__v_tolerance = search_vertical
        return Response()

    def get_search_windows(self):
        return AngleResponse(horizontal_angle=self.__hz_tolerance,
                             vertical_angle=self.__v_tolerance)

    def get_target(self):
        station = self.get_station()
        st = Point(station.easting,
                   station.northing,
                   station.height)
        angles = self.get_angles(atr=True)
        ta = polar.polar_to_grid(p1=st,
                                 distance=self.get_slope_distance().slope_distance,
                                 azimut=angles.horizontal_angle,
                                 zenith=angles.vertical_angle)

        return CoordinateResponse(easting=ta.x,
                                  northing=ta.y,
                                  height=ta.z)

    def switch_off(self):
        """

        :return:
        """
        return Response(description="Switch OFF")

    def switch_on(self):
        """

        :return:
        """
        return Response(description="Switch ON")

    def get_response(self):
        return Response(description="connected: %s" % self.__connected)

    def get_temperature(self):
        return TemperatureResponse(temperature=self.__temperature)

    def set_instrument_modes(self, atr_mode, edm_mode, hz_tolerance, v_tolerance):
        """

        :param atr_mode:
        :type atr_mode: int
        :param edm_mode:
        :type edm_mode: int
        :param hz_tolerance:
        :type hz_tolerance: float
        :param v_tolerance:
        :type v_tolerance: float
        :return:
        """
        self.__atr_mode = atr_mode
        self.__edm_mode = edm_mode
        self.__hz_tolerance = hz_tolerance
        self.__v_tolerance = v_tolerance
        return Response()

    def set_laser_pointer(self, value):
        """
        Schaltet den Laserpointer ein oder aus

        :param value:
        :return:
        """
        self.__laser_pointer = value
        return StateResponse(state=self.__laser_pointer)

    def get_laser_pointer(self):
        return StateResponse(state=self.__laser_pointer)

    def get_face(self):
        return StateResponse(state=self.__face)

    def get_prism_constant(self):
        return FloatResponse(value=self.__prism_constant)

    def get_reflector_height(self):
        return FloatResponse(value=self.__reflector_height)

    def get_instrument_number(self):
        return StringResponse(string=self.__instrument_number)

    def get_instrument_name(self):
        return StringResponse(string=self.__instrument_name)

    def get_station(self):
        return StationResponse(easting=self.__easting,
                               northing=self.__northing,
                               height=self.__height,
                               instrument_height=self.__instrument_height)

    def set_compensator_cross(self, value):
        self.__compensator_cross = value
        return Response()

    def set_compensator_length(self, value):
        self.__compensator_length = value
        return Response()

    def set_face(self, value):
        self.__face = value
        return Response()

    def set_orientation(self, value):
        self.__orientation = value
        return Response()

    def set_prism_constant(self, value):
        self.__prism_constant = value
        return Response()

    def set_reflector_height(self, value):
        self.__reflector_height = value
        return Response()

    def set_station(self, easting, northing, height, instrument_height):
        self.__easting = easting
        self.__northing = northing
        self.__height = height
        self.__instrument_height = instrument_height
        return Response()

    def connect(self):
        """

        :return:
        """
        return StateResponse(state=1)

    def clear(self):
        """
        Bereinige Speicher, Cache, etc.
        :return:
        """
        return StateResponse(state=1)

    def get_slope_distance(self):
        return DistanceResponse(slope_distance=self.__slope_distance + random.random()*1e-3)

    def get_ppm(self):
        return FloatResponse(value=random.random()*1e-4)

    def is_leveled(self):
        return StateResponse(state=1)
