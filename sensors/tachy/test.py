import unittest
import serial
import logging
import time

from leica.leica_tachy_tps1100 import TPS1100
from base import FACE_ONE, FACE_TWO, OFF

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LeicaTPS1100TachyTestCase(unittest.TestCase):

    def __init__(self, testname="runTest", port='/dev/ttyMXUSB0'):
        super(LeicaTPS1100TachyTestCase, self).__init__(testname)
        self.port = port

    def setUp(self):
        s = serial.Serial(port=self.port, timeout=7)
        if not s.isOpen():
            s.open()
        self.sensor = TPS1100(rs232=s)

    def test_brand(self):
        logger.debug("Testing brand 'Leica Geosystems'")
        r = self.sensor.get_brand()
        self.assertEqual(r["BRAND"], "Leica Geosystems",
                         msg="Sensor should be froom Leica Geosystems, got %s instead" % self.sensor.brand)

    def test_get_sensor_type(self):
        logger.debug("Testing sensor type 'TACHY'")
        r = self.sensor.get_sensor_type()
        r = self.sensor.get_sensor_type()
        self.assertEqual(r["SENSOR_TYPE"], "TACHY",
                         msg="Sensor should be a TACHY, got %s instead" % self.sensor.sensor_type)

    def test_get_response(self):
        logger.debug("Testing sensor NULL response")
        r = self.sensor.get_response()
        self.assertTrue(r["status"] == 200, msg="Statuscode is not 200")

    def test_get_sensor_name(self):
        logger.debug("Testing sensor name")
        r = self.sensor.get_instrument_name()
        logger.debug(r)
        self.assertTrue("T" in r["INSTRUMENT_NAME"],
                        msg="Sensor should be a TPS1100, got %s instead" % r["INSTRUMENT_NAME"])

    def test_change_face(self):
        logger.debug("Change tachy face")
        self.sensor.set_face(FACE_TWO)
        current_face = int(self.sensor.get_face()["FACE"])
        logger.info("FACE %d: " % current_face)
        self.assertEqual(int(FACE_TWO), current_face)
        logger.debug("Wait a few seconds")
        time.sleep(7)
        self.sensor.set_face(FACE_ONE)
        current_face = int(self.sensor.get_face()["FACE"])
        self.assertEqual(int(FACE_ONE), current_face)

    def test_message_to_logstash(self):
        """

        :return:
        """
        # TODO ..
        pass

    def tearDown(self):
        self.sensor.set_laser_pointer(OFF)
        # self.sensor.switch_off()
