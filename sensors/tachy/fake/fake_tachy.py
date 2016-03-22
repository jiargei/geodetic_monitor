# -*- coding: utf-8 -*-

# Third Party Module Import
import random

from serial import EIGHTBITS
from serial import PARITY_NONE
from serial import STOPBITS_ONE

# Package Import
from sensors.tachy.base import Tachy
from sensors.tachy import constants

from common.utils import generate


# Code


class FakeTachy(Tachy):

    def __init__(self, device):
        self.__connected = True if device == "/dev/null" else False
        self.__horizontal_angle = random.randint(0, 399) + random.random()*1e-1
        self.__vertical_angle = random.randint(0, 199) + random.random()*1e-1
        self.__slope_distance = random.randint(1, 540) + random.random()
        self.__laser_pointer = constants.OFF
        self.__face = constants.FACE_ONE
        self.__compensator_cross = random.random()*1e-4
        self.__compensator_length = random.random()*1e-4
        self.__prism_constant = constants.MODEL_TYPE_CHOICE[1]
        self.__reflector_height = 0.0
        self.__instrument_height = 0.0
        self.__instrument_number = random.randint(1000, 9999)
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

    def get_model_id(self):
        return 19

    def switch_off(self):
        """

        :return:
        """
        print "Switch OFF"

    def switch_on(self):
        """

        :return:
        """
        print "Switch ON"

    @staticmethod
    def get_tachymeter_type():
        return {"TACHYMETER_TYPE": "Fake Tachymeter"}

    def get_response(self):
        return self.__connected

    def get_temperature(self):
        return {"TEMPERATURE": self.__temperature}

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
        return {"LASERPOINTER": self.__laser_pointer}

    def get_angles(self, use_atr):
        """
        Liefert die Aktuellen Stellwinkel zurück
        :param use_atr:
        :return:
        """
        return {"HORIZONTAL_ANGLE": self.__horizontal_angle + random.random()*1e-3,
                "VERTICAL_ANGLE": self.__vertical_angle + random.random()*1e-3}

    def get_slope_distance(self):
        return {"SLOPE_DISTANCE": self.__slope_distance + random.random()*1e-4}

    def get_compensator_cross(self):
        return {'CROSS_INCLINE': self.__compensator_cross + random.random()*1e-5}

    def get_compensator_length(self):
        return {"LENGTH_INCLINE": self.__compensator_length + random.random()*1e-5}

    def get_face(self):
        return {"FACE": self.__face}

    def get_horizontal_angle(self):
        return {"HORIZONTAL_ANGLE": (self.__face*200 + self.__horizontal_angle + random.random()*1e-3) % 400}

    def get_prism_constant(self):
        return {"PRISM_CONSTANT": self.__prism_constant}

    def get_reflector_height(self):
        return {"REFLECTOR_HEIGHT": self.__reflector_height}

    def get_instrument_number(self):
        return {"INSTRUMENT_NUMBER": self.__instrument_number}

    def get_instrument_name(self):
        return {"INSTRUMENT_NAME": self.__instrument_name}

    def get_station(self):
        return {'EASTING': self.__easting,
                'NORTHING': self.__northing,
                'HEIGHT': self.__height,
                'INSTRUMENT_HEIGHT': self.__instrument_height}

    def get_vertical_angle(self):
        return {"VERTICAL_ANGLE": self.__vertical_angle if self.__face == 0 else 400 - self.__vertical_angle}

    def get_orientation(self):
        return {"ORIENTATION": self.__orientation}

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
        print "Seriennummer kann nicht verändert werden!"

    def set_instrument_name(self, value):
        print "Gerätename ist nicht veränderbar!"

    def set_slope_distance(self, value):
        self.__slope_distance = value

    def set_station(self, easting, northing, height, instrument_height):
        self.__easting = easting
        self.__northing = northing
        self.__height = height
        self.__instrument_height = instrument_height

    def set_vertical_angle(self, value):
        self.__vertical_angle = value

    def set_path(self, value):
        self.__path = value

    def get_path(self):
        return {"PATH": self.__path}

    def set_baudrate(self, value):
        self.__baudrate = value

    def get_baudrate(self):
        return {"BAUDRATE": self.__baudrate}

    def set_bytesize(self, value):
        self.__bytesize = value

    def get_bytesize(self):
        return {"BYTESIZE": self.__bytesize}

    def set_stopbits(self, value):
        self.__stopbits = value

    def get_stopbits(self):
        return {"STOPBITS": self.__stopbits}

    def set_parity(self, value):
        self.__parity = value

    def get_parity(self):
        return {"PARITY": self.__parity}

    def connect(self):
        """

        :return:
        """
        return {"SUCCESS": self.__connected}

    def clear(self):
        """
        Bereinige Speicher, Cache, etc.
        :return:
        """
        return {"SUCCESS": True}

    def turn_to(self, horizontal_angle, vertical_angle):
        """

        :param horizontal_angle:
        :param vertical_angle:
        :return:
        """
        self.__horizontal_angle = horizontal_angle + random.random()*1e-5
        self.__vertical_angle = vertical_angle + random.random()*1e-5

    def measure(self):
        return {"HORIZONTAL_ANGLE": self.get_horizontal_angle()["HORIZONTAL_ANGLE"],
                "VERTICAL_ANGLE": self.get_vertical_angle()["VERTICAL_ANGLE"],
                "SLOPE_DISTANCE": self.get_slope_distance()["SLOPE_DISTANCE"],
                "TEMPERATURE": self.get_temperature()["TEMPERATURE"],
                "FACE": self.get_face()["FACE"],
                "UID": generate.generate_id(),
                "PPM_CORR": random.random()*1e-4,
                "CROSS_INCLINE": self.get_compensator_cross()["CROSS_INCLINE"],
                "LENGTH_INCLINE": self.get_compensator_length()["LENGTH_INCLINE"],
                "REFLECTOR_HEIGHT": 0.0,
                "PRISM_CORR": constants.PrismConstant.PRISM_MINI,
                "CREATED": generate.generate_datestring()}

    def is_leveled(self):
        return True

