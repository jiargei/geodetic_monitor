# -*- coding: utf-8 -*-

__author__ = 'FJUE'

# Third Party Module Import
from abc import ABCMeta
from abc import abstractmethod
import time

# Package Import
from . import ABSTRACT_SENSOR
from ..constants import FACE
from ..tools import ANGLE

# Code
@property
def not_implemented_field(self):
    raise NotImplementedError


class Tachy(ABSTRACT_SENSOR.Sensor):
    """
    Abstrakte Klasse für Tachymeter
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_model_id(self):
        """
        Liefert Model ID
        :return:
        :rtype: int
        """

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

    @staticmethod
    def get_sensor_type():
        return {"SENSOR_TYPE": "TACHY"}

    @staticmethod
    def get_tachymeter_type():
        return {"TACHYMETER_TYPE": "Abstract Tachymeter"}

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
    def get_horizontal_angle(self):
        """
        Get Horizontal Angle
        :return:
        """

    @abstractmethod
    def set_horizontal_angle(self, value):
        """
        Set Horizontal Angle
        :param value:
        :return:
        """

    @abstractmethod
    def get_vertical_angle(self):
        """
        Get Vertical Angle
        :return:
        """

    @abstractmethod
    def set_vertical_angle(self, value):
        """
        Set Vertical Angle
        :return:
        """

    @abstractmethod
    def get_slope_distance(self):
        """
        Return Slope Distance
        :return:
        """

    @abstractmethod
    def set_slope_distance(self, value):
        """
        Set Slope Distance
        :param value:
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
    def get_compensator_cross(self):
        """
        Get Compensator Cross
        :return:
        """

    @abstractmethod
    def set_compensator_cross(self, value):
        """
        Set compenator cross value
        :param value:
        :return:
        """

    @abstractmethod
    def get_compensator_length(self):
        """
        Get Compensator Length
        :return:
        """

    @abstractmethod
    def set_compensator_length(self, value):
        """
        Set Compenator Length Value
        :param value:
        :return:
        """

    @abstractmethod
    def get_laser_pointer(self):
        """

        :return:
        """

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

    def turn_to_corr(self, horizontal_angle, vertical_angle, face):
        """
        Turn Tachymeter to hz, v and correct face

        :param horizontal_angle:
        :type horizontal_angle: float
        :param vertical_angle:
        :type vertical_angle: float
        :param face:
        :type face: int
        :return:
        """
        self.turn_to(horizontal_angle=ANGLE.change_face_hz(horizontal_angle, face),
                     vertical_angle=ANGLE.change_face_v(vertical_angle, face))
        #self.turn_to(horizontal_angle=horizontal_angle,
        #             vertical_angle=vertical_angle)

    @abstractmethod
    def turn_to(self, horizontal_angle, vertical_angle):
        """

        :param horizontal_angle:
        :param vertical_angle:
        :return:
        """

    def turn_to_measurement(self, measurement, face):
        """
        Drehe Tachymeter zu Messung

        :param measurement:
        :type measurement: dimosy.TACHY.MEASUREMENT.Measurement
        :return:
        """
        self.turn_to_corr(horizontal_angle=measurement.HORIZONTAL_ANGLE,
                          vertical_angle=measurement.VERTICAL_ANGLE,
                          face=face)

    def turn_to_reference(self, reference, face):
        """
        Drehe Tachymeter zu Referenz

        :param reference:
        :type reference: dimosy.TACHY.REFERENCE.Reference
        :return:
        """
        self.turn_to_corr(horizontal_angle=reference.HORIZONTAL_ANGLE,
                          vertical_angle=reference.VERTICAL_ANGLE,
                          face=face)

    @abstractmethod
    def measure(self):
        """
        Perform Measurement to aimed Target
        :return: HORIZONTAL_ANGLE, VERTICAL_ANGLE, SLOPE_DISTANCE, CREATED, UID
        :rtype: dict
        """

    @abstractmethod
    def set_orientation(self, value):
        """

        :param value:
        :return:
        """

    @abstractmethod
    def get_face(self):
        """

        :return:
        """

    @abstractmethod
    def change_face(self):
        """
        Wechselt Lage des Geräts
        """        

    def set_face(self, value):
        """

        :param value:
        :return:
        """
        self.correct_face(value)

    def correct_face(self, face):
        """
        Dreht Gerät in die Richtige Lage
        :param face: Gewünschte Lage
        :type face: int
        :return:
        """
        current_face = self.get_face()["FACE"]
        while not current_face == face:
            # print "Gerät ist in Lage %d, wechsle.." % current_face
            self.change_face()
            current_face = self.get_face()["FACE"]
            time.sleep(0.5)

        # print "Gerät ist in Lage %d" % current_face

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
        """

    @abstractmethod
    def clear(self):
        """
        Bereinige Instrument (Cache, Daten, etc.)
        :return:
        """

    @abstractmethod
    def get_angles(self, use_atr):
        """
        Liefert HZ und V des aktuellen Zieles
        :param use_atr: Verwende ATR oder nicht
        :type use_atr: bool
        :return:
        """

    @abstractmethod
    def get_orientation(self):
        """
        Liefert die Orientierung des Gerätes
        :return:
        """

    @abstractmethod
    def get_path(self):
        """

        :return:
        """

    @abstractmethod
    def set_path(self, value):
        """

        :param value:
        :return:
        """

    @abstractmethod
    def connect(self):
        """
        Versuche wiederholt, mit dem Tachymeter Kontakt herzustellen
        :return:
        :rtype: bool
        """

    @abstractmethod
    def disconnect(self):
        """
        Trenne serielle Verbindung mit Sensor
        :return:
        """

    @abstractmethod
    def is_leveled(self):
        """
        Prueft, ob der Tachymeter horizontiert ist.
        :return: True, wenn er horizontiert ist, sonst False
        :rtype: bool
        """

    @abstractmethod
    def set_baudrate(self, value):
        """

        :param value:
        :return:
        """

    @abstractmethod
    def get_baudrate(self):
        """

        :return:
        """

    @abstractmethod
    def set_bytesize(self, value):
        """

        :param value:
        :return:
        """

    @abstractmethod
    def get_bytesize(self):
        """

        :return:
        """

    @abstractmethod
    def set_stopbits(self, value):
        """

        :param value:
        :return:
        """

    @abstractmethod
    def get_stopbits(self):
        """

        :return:
        """

    @abstractmethod
    def set_parity(self, value):
        """

        :param value:
        :return:
        """

    @abstractmethod
    def get_parity(self):
        """

        :return:
        """
