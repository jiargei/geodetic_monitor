#!/bin/python
# -*- coding: utf-8 -*-

# Third Party Module Import
from abc import ABCMeta
from abc import abstractmethod, abstractproperty
import time
import imp
import os

# convert_path = str(os.getcwd()+"/geodetic/calculations/convert.py")
# print convert_path
# convert = imp.load_source("convert", convert_path)

from sensors.base import Sensor
from sensors import response
from geodetic.calculations import convert
from geodetic.calculations.polar import grid_to_polar
from geodetic.point import Point
from common.constants import FACE_ONE, FACE_TWO, OFF, ON



@property
def not_implemented_field(self):
    raise NotImplementedError


class Tachy(Sensor):
    """
    Abstrakte Klasse für Tachymeter
    """

    __metaclass__ = ABCMeta

    sensor_type = "TACHY"

    def __init__(self, connector, *args, **kwargs):
        super(Tachy, self).__init__(connector)
        self.search_hz = kwargs.get("search_hz", 100e-4)
        self.search_v = kwargs.get("search_v", 100e-4)
        self.__laserpointer_state = ON
        self.set_laser_pointer(self.__laserpointer_state)

    def __del__(self):
        self.set_laser_pointer(OFF)

    def set_polar(self, horizontal_angle, vertical_angle, aim_target=False):
        """

        :param horizontal_angle:
        :param vertical_angle:
        :param aim_target:
        :return:
        """
        return self.set_angles(horizontal_angle, vertical_angle, aim_target)


    @abstractmethod
    def set_search_windows(self, search_horizontal, search_vertical):
        """
        Setze Suchfenster für Tachymeter
        :param search_horizontal: Suchbereich Horizontalkreis
        :type search_horizontal: float
        :param search_vertical: Suchbereich Vertikalkreis
        :type search_vertical: float
        :return:
        """

    @abstractmethod
    def get_search_windows(self):
        """
        Liefert das Suchfenster
        :return: SEARCH_HORIZONTAL, SEARCH_VERTICAL
        :rtype: dict
        """

    @abstractmethod
    def switch_off(self):
        """
        Schaltet Tachymeter ab
        :return:
        """

    @abstractmethod
    def switch_on(self):
        """
        Schaltet Tachymeter ein
        :return:
        """

    @abstractmethod
    def get_response(self):
        """
        Prüft, ob Tachymeter erreichbar ist
        :return:
        :rtype: bool
        """

    @abstractmethod
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

    @abstractmethod
    def get_temperature(self):
        """

        :return:
        """

    @abstractmethod
    def get_instrument_number(self):
        """
        Return Serial Number
        :return:
        :rtype: str
        """

    @abstractmethod
    def set_instrument_number(self, value):
        """
        Set Serial Number
        :param value:
        :return:
        """

    @abstractmethod
    def get_instrument_name(self):
        """
        Return Instrument Name
        :return:
        :rtype: str
        """

    @abstractmethod
    def set_instrument_name(self, value):
        """
        Set Instrument name
        :param value:
        :return:
        """

    @abstractmethod
    def set_angles(self, hz, v, atr):
        """
        Set Vertical and Horizontal Angle

        :param hz:
        :param v:
        :param atr:
        :return:
        """

    @abstractmethod
    def get_prism_constant(self):
        """
        Get Instrument Prism Constant
        :return:
        """

    @abstractmethod
    def set_prism_constant(self, value):
        """
        Set Instrument Prism Constant
        :param value:
        :return:
        """

    @abstractmethod
    def get_compensator(self):
        """
        Get Compensator Length
        :return:
        :rtype: CompensatorResponse
        """

    def get_laser_pointer(self):
        """

        :return:
        """
        return response.StateResponse(self.__laserpointer_state)

    @abstractmethod
    def set_laser_pointer(self, value):
        """

        :param value: ON or OFF
        :type value: int
        :return:
        """

    @abstractmethod
    def set_reflector_height(self, value):
        """

        :param value:
        :return:
        """

    @abstractmethod
    def get_reflector_height(self):
        """

        :return:
        """

    def turn_to_corr(self, horizontal_angle, vertical_angle, face, atr=False):
        """
        Turn Tachymeter to hz, v and correct face

        :param horizontal_angle:
        :type horizontal_angle: float
        :param vertical_angle:
        :type vertical_angle: float
        :param face:
        :type face: int
        :param atr:
        :type atr: bool
        :return:
        """
        self.set_angles(horizontal_angle=convert.change_face_hz(horizontal_angle, face),
                        vertical_angle=convert.change_face_v(vertical_angle, face),
                        atr=atr)

    def turn_to_measurement(self, measurement, face):
        """
        Drehe Tachymeter zu Messung

        :param measurement:
        :type measurement: dimosy.TACHY.MEASUREMENT.Response
        :param face: In which face shall be measured
        :type face: int
        :return:
        """
        self.turn_to_corr(horizontal_angle=measurement.HORIZONTAL_ANGLE,
                          vertical_angle=measurement.VERTICAL_ANGLE,
                          face=face,
                          atr=False)

    def turn_to_reference(self, reference, face):
        """
        Drehe Tachymeter zu Referenz

        :param reference:
        :type reference: dimosy.TACHY.REFERENCE.Reference
        :param face:
        :type face: int
        :return:
        """
        self.turn_to_corr(horizontal_angle=reference.HORIZONTAL_ANGLE,
                          vertical_angle=reference.VERTICAL_ANGLE,
                          face=face,
                          atr=False)
        return response.Response()

    def turn_to_point(self, p, face):
        """

        :param p:
        :type p: Point
        :param face:
        :type face: int
        :return:
        """
        d_station = self.get_station()
        p_station = Point(x=d_station["EASTING"],
                          y=d_station["NORTHING"],
                          z=d_station["HEIGHT"]+d_station["INSTRUMENT_HEIGHT"])

        polar = grid_to_polar(p_station, p)
        self.turn_to_corr(horizontal_angle=polar["AZIMUT"],
                          vertical_angle=polar["ZENIT"],
                          face=face,
                          atr=False)

        return response.Response()

    def get_measurement(self):
        m1 = self.get_angles(atr=True)
        m2 = self.get_temperature()
        m3 = self.get_face()
        m4 = self.get_reflector_height()
        m5 = self.get_slope_distance()
        m6 = self.get_ppm()
        m7 = self.get_prism_constant()
        m = response.TachyMeasurementResponse(horizontal_angle=m1.horizontal_angle,
                                              vertical_angle=m1.vertical_angle,
                                              slope_distance=m5.slope_distance,
                                              temperature=m2.temperature,
                                              face=m3.state,
                                              uuid=m1.uuid,
                                              ppm=m6.value,
                                              reflector_height=m4.value,
                                              prism_constant=m7.value,
                                              created=m7.created
                                              )
        return m

    @abstractmethod
    def get_target(self):
        """
        Get Coordinates for aimed Target
        :return: EASTING, NORTHING, HEIGHT
        :rtype: CoordinateResponse
        """

    @abstractmethod
    def set_orientation(self, value):
        """
        Per definition of Leica... Change the recent azimut to corrected azimut
        Lets say Orientation is 112.4561 gon and the raw azimt = 3.4100 gon
        value should be 115.9661 gon

        :param value:
        :type value: float
        :return:
        """

    @abstractmethod
    def get_face(self):
        """

        :return:
        """

    def change_face(self):
        if self.get_face()["FACE"] == FACE_ONE:
            self.set_face(FACE_TWO)

        elif self.get_face()["FACE"] == FACE_TWO:
            self.set_face(FACE_ONE)

        return response.Response()

    @abstractmethod
    def set_face(self, value):
        """

        :param value:
        :return:
        """

    @abstractmethod
    def set_station(self, easting, northing, height, instrument_height):
        """

        :param easting:
        :param northing:
        :param height:
        :param instrument_height:
        :return:
        """

    @abstractmethod
    def get_station(self):
        """

        :return:
        :rtype: CoordinateResponse
        """

    def fine_adjust(self):
        """
        Ausrichten über Messpunkt mittels ATR
        """

    @abstractmethod
    def clear(self):
        """
        Bereinige Instrument (Cache, Daten, etc.)
        :return:
        """

    @abstractmethod
    def get_angles(self, atr):
        """
        Liefert HZ und V des aktuellen Zieles
        :param atr: Verwende ATR oder nicht
        :type atr: bool
        :return:
        :rtype: AngleResponse
        """

    @abstractmethod
    def get_slope_distance(self):
        """

        :return:
        :rtype: DistanceResponse
        """

    @abstractmethod
    def get_ppm(self):
        """

        :return:
        :rtype: FloatResponse
        """

    @abstractmethod
    def connect(self):
        """
        Versuche wiederholt, mit dem Tachymeter Kontakt herzustellen
        :return:
        :rtype: bool
        """

    @abstractmethod
    def is_leveled(self):
        """
        Prueft, ob der Tachymeter horizontiert ist.
        :return: True, wenn er horizontiert ist, sonst False
        :rtype: bool
        """
