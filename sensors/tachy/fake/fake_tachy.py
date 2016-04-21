# -*- coding: utf-8 -*-

# Third Party Module Import
import random

from serial import EIGHTBITS
from serial import PARITY_NONE
from serial import STOPBITS_ONE

# Package Import
from sensors.tachy.base import Tachy
from sensors.tachy import base
from geodetic.calculations import polar
from geodetic.point import Point

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
        self.__laser_pointer = base.OFF
        self.__face = base.FACE_ONE
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
        self.__level = True

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
        return {"status": 200, "description": "Aiming at target"}

    def get_compensator(self):
        d = {
            "COMPENSATOR_CROSS": self.__compensator_cross,
            "COMPENSATOR_LENGTH": self.__compensator_length
        }
        return d

    def set_angles(self, hz, v, atr):
        """

        :param hz:
        :param v:
        :param atr:
        :return:
        """
        self.__horizontal_angle = hz
        self.__vertical_angle = v

    def get_angles(self, use_atr):
        """
        Liefert die Aktuellen Stellwinkel zurück
        :param use_atr:
        :return:
        """
        eps_hz = random.random()*4e-4 if use_atr else random.random()*2e-3
        eps_v = random.random()*4e-4 if use_atr else random.random()*2e-3

        return {
            "status": 200,
            "HORIZONTAL_ANGLE": self.__horizontal_angle + eps_hz,
            "VERTICAL_ANGLE": self.__vertical_angle + eps_v
        }

    def set_search_windows(self, search_horizontal, search_vertical):
        self.__hz_tolerance = search_horizontal
        self.__v_tolerance = search_vertical

    def get_search_windows(self):
        return {
            "status": 200,
            "SEARCH_VERTICAL": self.__hz_tolerance,
            "SEARCH_HORIZONTAL": self.__v_tolerance,
        }

    def get_target(self):
        d = {
            "status": 200,
            "EASTING": self.__easting,
            "NORTHING": self.__northing,
            "HEIGHT": self.__height
        }
        return d

    def switch_off(self):
        """

        :return:
        """
        return {"status": 200, "description": "Switch OFF"}

    def switch_on(self):
        """

        :return:
        """
        return {"status": 200, "description": "Switch ON"}

    def get_response(self):
        return {
            "status": 200,
            "description": "connected: %s" % self.__connected
        }

    def get_temperature(self):
        return {
            "status": 200,
            "TEMPERATURE": self.__temperature
        }

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

    def set_laser_pointer(self, value):
        """
        Schaltet den Laserpointer ein oder aus

        :param value:
        :return:
        """
        self.__laser_pointer = value

    def get_laser_pointer(self):
        return {"status": 200, "LASERPOINTER": self.__laser_pointer}

    def get_face(self):
        return {"status": 200, "FACE": self.__face}

    def get_prism_constant(self):
        return {"status": 200, "PRISM_CONSTANT": self.__prism_constant}

    def get_reflector_height(self):
        return {"status": 200, "REFLECTOR_HEIGHT": self.__reflector_height}

    def get_instrument_number(self):
        return {"status": 200, "INSTRUMENT_NUMBER": self.__instrument_number}

    def get_instrument_name(self):
        return {"status": 200, "INSTRUMENT_NAME": self.__instrument_name}

    def get_station(self):
        return {
            "status": 200,
            'EASTING': self.__easting,
            'NORTHING': self.__northing,
            'HEIGHT': self.__height,
            'INSTRUMENT_HEIGHT': self.__instrument_height
        }

    def set_compensator_cross(self, value):
        self.__compensator_cross = value

    def set_compensator_length(self, value):
        self.__compensator_length = value

    def set_face(self, value):
        self.__face = value

    def set_orientation(self, value):
        self.__orientation = value

    def set_prism_constant(self, value):
        self.__prism_constant = value

    def set_reflector_height(self, value):
        self.__reflector_height = value

    def set_station(self, easting, northing, height, instrument_height):
        self.__easting = easting
        self.__northing = northing
        self.__height = height
        self.__instrument_height = instrument_height

    def connect(self):
        """

        :return:
        """
        return {"status": 200, "SUCCESS": self.__connected}

    def clear(self):
        """
        Bereinige Speicher, Cache, etc.
        :return:
        """
        return {"status": 200, "SUCCESS": True}

    def get_measurement(self):
        d = {
            "status": 200,
            "HORIZONTAL_ANGLE": self.__horizontal_angle + random.random()*1e-4,
            "VERTICAL_ANGLE": self.__vertical_angle + random.random()*1e-4,
            "SLOPE_DISTANCE": self.__slope_distance + random.random()*1e-3,
            "TEMPERATURE": self.get_temperature()["TEMPERATURE"],
            "FACE": self.get_face()["FACE"],
            "UID": generate.generate_id(),
            "PPM_CORR": random.random()*1e-4,
            "REFLECTOR_HEIGHT": 0.0,
            "PRISM_CORR": self.__prism_constant,
            "CREATED": generate.generate_datestring()
        }
        d.update(self.get_compensator())
        d.update(b.create_date())
        d.update(b.create_uid())
        return d

    def is_leveled(self):
        return {
            "status": 200,
            "description": "Leveled: %s" % self.__level
        }
