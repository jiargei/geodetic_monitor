# -*- coding: utf-8 -*-

# Third Party Module Import
import time

# Package Import
from sensors.tachy.base import Tachy
import tmc
import aut
import geocom


class LeicaTachy(Tachy):

    brand = "Leica Geosystems"

    def __init__(self, serial):
        """

        :param serial: Serial
        :return:
        """
        self.serial = serial

    def clear(self):
        """

        :return:
        """
        self.communicate(geocom.COM_NullProc())
        self.communicate(geocom.TMC_DoMeasure(tmc.TMC_CLEAR))

    def communicate(self, geocom_command):
        """

        :param geocom_command: GeoCOMCommand
        :return:
        """
        self.serial.write(str(geocom_command))
        geocom_command.set_serial_read(self.serial.readline())
        return geocom_command.execute()

    def get_measurement(self):
        """

        :return:
        """
        self.communicate(geocom.TMC_DoMeasure(tmc.TMC_CLEAR))
        self.communicate(geocom.TMC_DoMeasure(tmc.TMC_DEF_DIST))
        return self.communicate(geocom.TMC_GetSimpleMea())

    def fine_adjust(self):
        """

        :return:
        """
        return self.communicate(geocom.AUT_FineAdjust())

    def get_response(self):
        """

        :return:
        """
        return self.communicate(geocom.COM_NullProc())

    def set_reflector_height(self, value):
        return self.communicate(geocom.TMC_SetHeight(value))

    def get_reflector_height(self):
        return self.communicate(geocom.TMC_GetHeight())

    def set_station(self, easting, northing, height, instrument_height):
        return self.communicate(geocom.TMC_SetStation(easting, northing, height))

    def get_station(self):
        return self.communicate(geocom.TMC_GetStation())

    def set_face(self, value):
        while value != self.communicate(geocom.TMC_GetFace())['FACE']:
            cmd = self.communicate(geocom.AUT_ChangeFace())
            time.sleep(1)

    def get_face(self):
        return self.communicate(geocom.TMC_GetFace())

    def set_orientation(self, orientation):
        return self.communicate(geocom.TMC_SetOrientation(orientation))

    def set_polar(self, horizontal_angle, vertical_angle, aim_target=False):
        if aim_target:
            atr_mode = aut.AUT_TARGET
        else:
            atr_mode = aut.AUT_POSITION
        return self.communicate(geocom.AUT_MakePositioning(horizontal_angle,
                                                           vertical_angle,
                                                           atr_mode))

    def get_polar(self):
        get_hzv = self.communicate(geocom.TMC_GetAngle1())
        self.communicate(geocom.TMC_DoMeasure(measurement_mode=tmc.TMC_DEF_DIST,
                                              inclination_mode=tmc.TMC_MEA_INC))

    def set_prism_constant(self, value):
        """

        :param value:
        :return:
        """
        self.communicate(geocom.BAP_SetPrismType(prism_type=value))

    def set_compensator_cross(self, value):
        """
        Kompensator kann nicht manuell gesetzt werden

        :param value:
        :return:
        """
        "Kompensator kann manuel nicht gesetzt werden"

    def set_compensator_length(self, value):
        """
        Kompensator kann nicht manuell gesetzt werden

        :param value:
        :return:
        """
        "Kompensator kann manuel nicht gesetzt werden"

    def get_prism_constant(self):
        """

        :return:
        """
        return self.communicate(geocom.TMC_GetPrismCorr())

    def get_temperature(self):
        """

        :return:
        """
        return self.communicate(geocom.CSV_GetIntTemp())

    def switch_off(self):
        """

        :return:
        """
        return self.communicate(geocom.COM_SwitchOffTPS(on_off=1))

    def switch_on(self):
        """

        :return:
        """
        return self.communicate(geocom.COM_SwitchOffTPS(on_off=0))

    def get_instrument_name(self):
        """

        :return:
        """
        return self.communicate(geocom.CSV_GetInstrumentName())

    def get_instrument_number(self):
        """

        :return:
        """
        return self.communicate(geocom.CSV_GetInstrumentNo())
