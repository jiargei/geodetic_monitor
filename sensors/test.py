import unittest
from abc import ABCMeta, abstractmethod


class SensorTestCase(unittest.TestCase):

    __metaclass__ = ABCMeta

    @abstractmethod
    def test_brand(self):
        pass

    @abstractmethod
    def test_get_sensor_type(self):
        pass

    @abstractmethod
    def test_get_response(self):
        pass

    @abstractmethod
    def test_get_sensor_name(self):
        pass
