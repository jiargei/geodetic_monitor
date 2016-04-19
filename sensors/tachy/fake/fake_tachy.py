# -*- coding: utf-8 -*-

# Third Party Module Import
import random

from serial import EIGHTBITS
from serial import PARITY_NONE
from serial import STOPBITS_ONE

# Package Import
from sensors.tachy.base import Tachy
from sensors.tachy import base

from sensors import base as b

from common.utils import generate


# Code


class FakeTachy(Tachy):

    brand = "FaKeBrAnD"
    model = "FaKeMoDeL"

    def __init__(self, device, *args, **kwargs):
        super(FakeTachy, self).__init__(*args, **kwargs)
        self.__connected = True if device == "/dev/null" else False
        self.__horizontal_angle = random.randint(0, 399) + random.random()*1e-1
        self.__vertical_angle = random.randint(0, 199) + random.random()*1e-1
        self.__slope_distance = random.randint(1, 540) + random.random()
        self.__laser_pointer = base.OFF
        self.__face = base.FACE_ONE
        self.__compensator_cross = random.random()*1e-4
        self.__compensator_length = random.random()*1e-4
        self.__prism_constant = 0.0175
        self.__reflector_height = 0.0
        self.__instrument_height = 0.0
        self.__instrument_number = "95173"
        self.__instrument_name = "Fake Tachymeter v0.1"
        self.__easting = random.randint(-3000, 4000) + random.random()*1e2
        self.__northing = random.randint(336200, 336999) + random.random()*1e2
        self.__height = random.randint(156, 240) + random.random()*1e1
        self.__orientation = random.randint(0, 399) + random.random()*1e-1
        self.__temperature = random.randint(-1, 18) + random.random()*1e-1
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

    @property
    def model_type(self):
        return "Fake"

    def get_compensator(self):
        d = {
            "COMPENSATOR_CROSS": self.__compensator_cross,
            "COMPENSATOR_LENGTH": self.__compensator_length
        }
        return d

    def set_level(self, value):
        assert isinstance(value, bool)
        self.__level = value

    def set_angles(self, hz, v, atr):
        self.__horizontal_angle = hz
        self.__vertical_angle = v

    def set_polar(self, horizontal_angle, vertical_angle, aim_target=False):
        self.set_angles(horizontal_angle, vertical_angle, aim_target)

    def set_search_windows(self, search_horizontal, search_vertical):
        self.__hz_tolerance = search_horizontal
        self.__v_tolerance = search_vertical

    def get_target(self):
        d = {
            "status": 200,
            "EASTING": self.__easting,
            "NORTHING": self.__northing,
            "HEIGHT": self.__height
        }

    def get_search_windows(self):
        return {
            "status": 200,
            "SEARCH_VERTICAL": self.__hz_tolerance,
            "SEARCH_HORIZONTAL": self.__v_tolerance,
        }

    def get_model_id(self):
        return 19

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

    def get_angles(self, use_atr):
        """
        Liefert die Aktuellen Stellwinkel zurück
        :param use_atr:
        :return:
        """
        return {
            "status": 200,
            "HORIZONTAL_ANGLE": self.__horizontal_angle + random.random()*1e-3,
            "VERTICAL_ANGLE": self.__vertical_angle + random.random()*1e-3
        }

    def get_slope_distance(self):
        return {"status": 200, "SLOPE_DISTANCE": self.__slope_distance + random.random()*1e-4}

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

    def get_orientation(self):
        return {"status": 200, "ORIENTATION": self.__orientation}

    def set_compensator_cross(self, value):
        self.__compensator_cross = value

    def set_compensator_length(self, value):
        self.__compensator_length = value

    def set_face(self, value):
        self.__face = value

    def set_horizontal_angle(self, value):
        self.__horizontal_angle = value

    def set_instrument(self, atr_mode, edm_mode, hz_tolerance, v_tolerance):
        pass

    def set_orientation(self, value):
        self.__orientation = value

    def set_prism_constant(self, value):
        self.__prism_constant = value

    def set_reflector_height(self, value):
        self.__reflector_height = value

    def set_instrument_number(self, value):
        return {
            "status": 200,
            "description": "Seriennummer kann nicht verändert werden!"
        }

    def set_instrument_name(self, value):
        return {
            "status": 200,
            "description": "Gerätename ist nicht veränderbar!"
        }

    def set_slope_distance(self, value):
        self.__slope_distance = value

    def set_station(self, easting, northing, height, instrument_height):
        self.__easting = easting
        self.__northing = northing
        self.__height = height
        self.__instrument_height = instrument_height

    def set_vertical_angle(self, value):
        self.__vertical_angle = value

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

    def turn_to(self, horizontal_angle, vertical_angle):
        """

        :param horizontal_angle:
        :param vertical_angle:
        :return:
        """
        self.__horizontal_angle = horizontal_angle + random.random()*1e-5
        self.__vertical_angle = vertical_angle + random.random()*1e-5

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

