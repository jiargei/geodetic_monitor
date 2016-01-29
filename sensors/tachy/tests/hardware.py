import unittest

import serial

from sensors.tachy.hardware.leica import LeicaTachy


class TestLeicaTachyMethods(unittest.TestCase):
    """

    """
    def setUp(self):
        """

        :return:
        """
        s = serial.Serial(port='/dev/ttyMXUSB2')
        if not s.isOpen():
            s.open()

        self.tachy = LeicaTachy(s)

    def test_response(self):
        self.assertEqual(self.tachy.get_response()['status'], 200)

