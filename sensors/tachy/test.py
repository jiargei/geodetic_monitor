import serial
import logging

from leica.leica_tachy_tps1100 import TPS1100
from fake.fake_tachy import FakeTachy
from ..test import TachySensorTestCase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LeicaTPS1100TachyTestCase(TachySensorTestCase):

    def __init__(self, testname="runTest", port='/dev/ttyMXUSB0'):
        super(LeicaTPS1100TachyTestCase, self).__init__(testname)
        self.port = port

    def setUp(self):
        s = serial.Serial(port=self.port, timeout=7)
        if not s.isOpen():
            s.open()
        self.sensor = TPS1100(connector=s)

    def test_get_sensor_name(self):
        logger.debug("Testing sensor name")
        r = self.sensor.get_instrument_name()
        logger.debug(r)
        self.assertTrue("T" in r["INSTRUMENT_NAME"],
                        msg="Sensor should be a TPS1100, got %s instead" % r.string)

    def test_message_to_logstash(self):
        """

        :return:
        """
        # TODO ..
        pass


class FakeTachySensorTestCase(TachySensorTestCase):

    def __init__(self, *args, **kwargs):
        super(FakeTachySensorTestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        self.sensor = FakeTachy(connector='/dev/null')

    def test_get_sensor_name(self):
        logger.debug("Testing sensor name")
        r = self.sensor.get_instrument_name()
        logger.debug(r)
        self.assertTrue("Fake" in r.string,
                        msg="Sensor should be a Fake, got %s instead" % r.string)
