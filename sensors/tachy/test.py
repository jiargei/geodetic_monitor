import unittest
import serial

from leica.leica_tachy_tps1100 import TPS1100


class LeicaTPS1100TachyTestCase(unittest.TestCase):

    def __init__(self, testname="runTest", port='/dev/ttyMXUSB1'):
        super(LeicaTPS1100TachyTestCase, self).__init__(testname)
        self.port = port

    def setUp(self):
        s = serial.Serial(port=self.port)
        if not s.isOpen():
            s.open()
        self.sensor = TPS1100(serial=s)

    def test_brand(self):
        r = self.sensor.get_brand()
        self.assertEqual(r["BRAND"], "Leica Geosystems",
                         msg="Sensor should be froom Leica Geosystems, got %s instead" % self.sensor.brand)

    def test_get_sensor_type(self):
        r = self.sensor.get_sensor_type()
        self.assertEqual(r["SENSOR_TYPE"], "TACHY",
                         msg="Sensor should be a TACHY, got %s instead" % self.sensor.sensor_type)

    def test_get_response(self):
        r = self.sensor.get_response()
        self.assertTrue(r["status"] == 200, msg="Statuscode ist nicht 200")

    def test_get_sensor_name(self):
        r = self.sensor.get_instrument_name()
        self.assertTrue("TPS" in r["INSTRUMENT_NAME"],
                        msg="Sensor should be a TPS1100, got %s instead" % r["INSTRUMENT_NAME"])
