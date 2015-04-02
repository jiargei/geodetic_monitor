# -*- coding: utf-8 -*-

__author__ = 'FJUE'

# Third Party Module Import


# Package Import
import TACHY_LEICA_11
import TACHY_LEICA_16
import TACHY_LEICA_18
import TACHY_FAKE
from ..constants import TACHY_TYPES


# Code
class TachyFactory(object):

    def __init__(self, baudrate, bytesize, stopbits, device, address, parity):
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.stopbits = stopbits
        self.device = device
        self.address = address
        self.partiy = parity

    def new_tachy(self, tachy_type):
        """
        Liefert einen Tachysensor

        :param tachy_type:
        :type tachy_type: int
        :return: Tachymeter Sensor
        :rtype: dimosy.TACHY.TACHY.Tachy
        """
        assert isinstance(tachy_type, int)

        # Leica TPS1100 und TS15
        if tachy_type in [TACHY_TYPES.LEICA_TPS11,
                          TACHY_TYPES.LEICA_TS15]:
            return TACHY_LEICA_11.LeicaTachy11(self.device,
                                               self.baudrate,
                                               self.bytesize,
                                               self.stopbits)

        # Leica TS15 mit Radiohandle
        elif tachy_type in [TACHY_TYPES.LEICA_TS15_WITH_RADIOHANDLE]:
            return TACHY_LEICA_16.LeicaTachy16(self.device,
                                               self.baudrate,
                                               self.bytesize,
                                               self.stopbits)

        # Leica TCA1800
        elif tachy_type in [TACHY_TYPES.LEICA_TCA18]:
            return TACHY_LEICA_18.LeicaTachy18(self.device,
                                               self.baudrate,
                                               self.bytesize,
                                               self.stopbits)

        # Fake Tachymeter
        elif tachy_type in [TACHY_TYPES.FAKE_TACHY]:
            return TACHY_FAKE.FakeTachy(self.device)

        raise NotImplementedError
