# -*- coding: utf-8 -*-

__author__ = 'FJUE'

# Third Party Module Import
from abc import ABCMeta
from abc import abstractmethod

# Package Import
from ..tools import GENERATES

# Code
@property
def not_implemented_field(self):
    raise NotImplementedError


class Sensor(object):
    """
    diese Klasse soll als Interface für Sensoren Tachymeter, Disto, Neigungssensor, Meteo gedacht sein

    """
    # baudrate = not_implemented_field
    # stopbits = not_implemented_field
    # bytesize = not_implemented_field
    # parity = not_implemented_field
    # address = not_implemented_field
    # path = not_implemented_field

    __metaclass__ = ABCMeta

    def __init__(self):
        self.__UID = GENERATES.gen_uuid()

    @abstractmethod
    def get_response(self):
        """
        Prüft, ob Tachymeter erreichbar ist
        :return:
        :rtype: bool
        """

    @staticmethod
    def get_sensor_type():
        """
        Liefert den Sensor-Type (TACHY, DISTO, NIVEL, METEO, etc.)
        :return: SENSOR_TYPE
        :rtype: dict
        """
        raise NotImplementedError

    @abstractmethod
    def get_instrument_number(self):
        """

        :return: INSTRUMENT_NUMBER
        :rtype: dict
        """

    @abstractmethod
    def get_instrument_name(self):
        """

        :return: INSTRUMENT_NAME
        :rtype: dict
        """

    @abstractmethod
    def clear(self):
        """
        Löscht Cache bzw. vorherige Eingaben
        :return:
        """

    @abstractmethod
    def connect(self):
        """
        Verbindet mit dem Sensor
        :return:
        """

    @abstractmethod
    def disconnect(self):
        """
        Trennt Verbindung mit Sensor
        :return:
        """

    @abstractmethod
    def measure(self):
        """
        Führt je nach Sensortyp eine Messung aus und liefert Attribute + Werte in form eines dicts
        :return:
        :rtype: dict
        """

    @abstractmethod
    def switch_off(self):
        """
        Schaltet Sensor ab
        :return:
        """

    @abstractmethod
    def switch_on(self):
        """
        Schaltet Sensor ein
        :return:
        """
