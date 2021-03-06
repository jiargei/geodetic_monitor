import unittest
from abc import ABCMeta, abstractmethod
import logging
import time
from constants import RESPONSE_SUCCESS
from constants import FACE_ONE, FACE_TWO, OFF

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SensorTestCase(unittest.TestCase):

    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        super(SensorTestCase, self).__init__(*args, **kwargs)
        self.sensor = None

    @abstractmethod
    def test_brand(self):
        pass

    @abstractmethod
    def test_get_sensor_type(self):
        pass

    def test_get_response(self):
        logger.debug("Testing sensor NULL response")
        r = self.sensor.get_response()
        self.assertTrue(r.status == RESPONSE_SUCCESS, msg="Status code is not %d" % RESPONSE_SUCCESS)

    @abstractmethod
    def test_get_sensor_name(self):
        pass

    @abstractmethod
    def test_get_measurement(self):
        pass


class TachySensorTestCase(SensorTestCase):

    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        super(TachySensorTestCase, self).__init__(*args, **kwargs)

    def test_get_sensor_type(self):
        logger.debug("Testing sensor type 'TACHY'")
        r = self.sensor.get_sensor_type()
        self.assertEqual(r.string, "TACHY",
                         msg="Sensor should be a TACHY, got %s instead" % self.sensor.sensor_type)

    def test_change_face(self):
        logger.debug("Change tachy face")
        self.sensor.set_face(FACE_TWO)
        current_face = int(self.sensor.get_face().state)
        # logger.info("FACE %d: " % current_face)
        self.assertEqual(int(FACE_TWO), current_face)
        logger.debug("Wait a few seconds")
        time.sleep(4)
        self.sensor.set_face(FACE_ONE)
        current_face = int(self.sensor.get_face().state)
        self.assertEqual(int(FACE_ONE), current_face)

    def test_brand(self):
        logger.debug("Testing brand '%s'" % self.sensor.brand)
        r = self.sensor.get_brand()
        self.assertEqual(r.string, self.sensor.brand,
                         msg="Sensor should be from Leica Geosystems, got %s instead" % self.sensor.brand)

    def test_get_angles(self):
        angles = self.sensor.get_angles(atr=False)
        self.assertTrue(angles.status == RESPONSE_SUCCESS)

    def test_get_angles(self):
        r = self.sensor.get_angles(atr=False)
        self.assertEqual(r.status, RESPONSE_SUCCESS)

    def test_get_measurement(self):
        r = self.sensor.get_measurement()
        self.assertTrue(r.status == RESPONSE_SUCCESS)

    def tearDown(self):
        self.sensor.set_laser_pointer(OFF)
        # self.sensor.switch_off()
