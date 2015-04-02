# -*- coding: utf-8 -*-

__author__ = 'FJUE'

# Third Party Module Import
import time

# Package Import
from . import TACHY, VARS
from ..geocom import GEOCOM, TMC
from ..constants import MAIN
from ..tools import GENERATES

# Code
class LeicaTachy16(TACHY.Tachy):
    """
    Klasse für TS15 mit RadioHandle - kann nicht ausgeschalten werden
    """

    def get_model_id(self):
        return 16

    def __init__(self, device, baudrate, bytesize, stopbits):
        self.tps = GEOCOM.GeoCOM(BAUDRATE=baudrate,
                           STOPBITS=stopbits,
                           BYTESIZE=bytesize,
                           PATH=device)
        self.__laserpointer = MAIN.OFF

    def switch_off(self):
        """

        :return:
        """
        print "Gerät mit Radiohandle kann nicht abgeschalten werden"

    def switch_on(self):
        """

        :return:
        """
        self.tps.COM_SwitchOnTPS()

    @staticmethod
    def get_tachymeter_type():
        return {"TACHYMETER_TYPE": "Leica Tachymeter"}

    def get_response(self):
        return self.tps.COM_NullProc()

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
        self.tps.set_tps(ATR_MODE=atr_mode,
                         EDM_MODE=edm_mode,
                         TOL_HZ=hz_tolerance,
                         TOL_V=v_tolerance)

    def get_instrument_number(self):
        """

        :return:
        """
        return self.tps.CSV_GetInstrumentNo()

    def get_instrument_name(self):
        """

        :return:
        """
        return self.tps.CSV_GetInstrumentName()

    def get_compensator_cross(self):
        """

        :return:
        """
        tmp = self.tps.TMC_GetAngle1()
        return {'CROSS_INCLINE': tmp['CROSS_INCLINE']}

    def get_compensator_length(self):
        """

        :return:
        """
        tmp = self.tps.TMC_GetAngle1()
        return {'LENGTH_INCLINE': tmp['LENGTH_INCLINE']}

    def get_angles(self, use_atr):
        """
        Liefert die aktuellen Stellwinkel beruecksichtigt dabei, ob ATR verwendet werden soll oder nicht

        :param use_atr: ATR
        :type use_atr: bool
        :return:
        """
        tmp = self.tps.TMC_GetAngle5()
        return {'HORIZONTAL_ANGLE': tmp['HORIZONTAL_ANGLE'],
                'VERTICAL_ANGLE': tmp['VERTICAL_ANGLE']}

    def get_horizontal_angle(self):
        """

        :return:
        """
        tmp = self.tps.TMC_GetAngle5()
        return {'HORIZONTAL_ANGLE': tmp['HORIZONTAL_ANGLE']}

    def get_vertical_angle(self):
        """

        :return:
        """
        tmp = self.tps.TMC_GetAngle5()
        return {'VERTICAL_ANGLE': tmp['VERTICAL_ANGLE']}

    def set_laser_pointer(self, value):
        """
        Schaltet Laserpointer ein oder aus
        :param value: 1..ein, 0..aus
        :type value: str
        :return:
        """

        assert value in [MAIN.ON, MAIN.OFF]
        if value == MAIN.ON:
            tmp = self.tps.EDM_Laserpointer_ON()

        elif value == MAIN.OFF:
            tmp = self.tps.EDM_Laserpointer_OFF()

        self.__laserpointer = value
        return {"RESULT": tmp}

    def get_reflector_height(self):
        """

        :return:
        """
        return {'REFLECTOR_HEIGHT': self.tps.TMC_GetHeight()["REFLECTOR_HEIGHT"]}

    def set_reflector_height(self, value):
        """

        :param value:
        :return:
        """
        return {"RESULT": self.tps.TMC_SetHeight(REFLECTOR_HEIGHT=value)}

    def set_orientation(self, value):
        """

        :param value:
        :return:
        """
        self.tps.TMC_SetOrientation(value)

    def get_face(self):
        """

        :return:
        """
        return {"FACE": self.tps.TMC_GetFace()["FACE"]}

    def get_slope_distance(self):
        """
        Liefert die gemessene Schraegstecke
        :return:
        """
        setter_dict = ["self.TMC_DoMeasure(TMC.TMC_CLEAR, EDM.EDM_SINGLE_TAPE)",
                       "self.TMC_DoMeasure(%d, %d)" % (TMC.TMC_DEF_DIST, TMC.TMC_AUTO_INC)]

        getter_dict = ["self.TMC_GetSimpleMea(%d, %d)" % (MAIN.WAIT_TIME, TMC.TMC_AUTO_INC),
                       "self.TMC_DoMeasure(TMC.TMC_CLEAR, EDM.EDM_SINGLE_TABE"]

        tmp = self.tps.do_dict(setter_dict=setter_dict,
                               getter_dict=getter_dict,
                               command_retry=MAIN.COMMAND_RETRIES,
                               command_wait=MAIN.COMMAND_WAIT)

        return {"SLOPE_DISTANCE": tmp["SLOPE_DISTANCE"]}

    def get_station(self):
        """

        :return:
        """
        return self.tps.TMC_GetStation()

    def get_orientation(self):
        """

        :return:
        """
        pass

    def get_laser_pointer(self):
        """

        :return:
        """
        return {"LASERPOINTER": self.__laserpointer}

    def get_prism_constant(self):
        """

        :return:
        """
        return {"PRISM_CONSTANT": self.tps.TMC_GetPrismCorr()["PRISM_CORR"]}

    def measure(self):
        """

        :return:
        """
        return {'UID':GENERATES.gen_uuid(),
                'CREATED': GENERATES.gen_now(DATE_RETURN=True)}.update(self.tps.BAP_MeasDistanceAngle())

    def connect(self):
        """

        :return:
        """
        # Versuche wiederholt, mit dem Tachymeter Kontakt herzustellen
        try_to_connect = 0
        while not self.tps.COM_NullProc() and try_to_connect <= VARS.NULL_PRO_RETRY_ATTEMP:
            time.sleep(VARS.NULL_PRO_RETRY_TIME)
            try_to_connect += 1
        return self.tps.COM_NullProc()

    def disconnect(self):
        del self.tps

    def is_leveled(self):
        """
        Prüft, ob das Gerät horizontiert ist.

        :return: True, wenn der Tachymeter horizontiert ist, sonst False
        :rtype: bool
        """
        return self.tps.is_horizonted()
