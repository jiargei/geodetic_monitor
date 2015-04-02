# -*- coding: utf-8 -*-

__author__ = 'FJUE'

# Third Party Module Import
import time

# Package Import
from . import TACHY, VARS
from ..constants import MAIN
from ..geocom import TMC, BAP, GEOCOM
from ..tools import GENERATES


# Code
class LeicaTachy11(TACHY.Tachy):
    """

    """

    def __init__(self, device, baudrate, bytesize, stopbits):
        self.tps = GEOCOM.GeoCOM(BAUDRATE=baudrate,
                                 STOPBITS=stopbits,
                                 BYTESIZE=bytesize,
                                 PATH=device)
        self.__laserpointer = MAIN.OFF
        self.__search_horizontal = 40e-4
        self.__search_vertical = 40e-4

    def get_model_id(self):
        return 11

    def clear(self):
        """

        :return:
        """
        self.tps.TMC_DoMeasure(TMC_Mode=TMC.TMC_CLEAR)

    def change_face(self):
        """
        """
        self.tps.AUT_ChangeFace()

    def set_baudrate(self, value):
        """

        :param value:
        :type value: int
        :return:
        """
        self.tps.BAUDRATE = value

    def set_bytesize(self, value):
        """

        :param value:
        :type value: int
        :return:
        """
        self.tps.BYTESIZE = value

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

    def set_horizontal_angle(self, value):
        """
        Stellt Gerät auf Horizontalwinkel
        :param value: Horizontalwinkel
        :type value: float
        :return:
        """
        self.tps.turn_to(HORIZONTAL_ANGLE=value,
                         VERTICAL_ANGLE=self.get_vertical_angle()["VERTICAL_ANGLE"])

    def set_vertical_angle(self, value):
        """
        Stellt Gerät auf Vertikalwinkel

        :param value: Vertikalwinkel
        :type value: float
        """
        self.tps.turn_to(HORIZONTAL_ANGLE=self.get_horizontal_angle()["HORIZONTAL_ANGLE"],
                         VERTICAL_ANGLE=value)

    def set_instrument_name(self, value):
        """

        :param value:
        :return:
        """
        "Gerätename kann nicht geändert werden"

    def set_instrument_number(self, value):
        """

        :param value:
        :return:
        """
        "Gerätenummer kann nicht geärndert werden"

    def set_parity(self, value):
        """

        :param value:
        :type value: str
        :return:
        """
        self.tps.PARITY = value

    def set_path(self, value):
        """

        :param value:
        :type value: str
        :return:
        """
        self.tps.PATH = value

    def set_prism_constant(self, value):
        """

        :param value:
        :type value: int
        :return:
        """
        self.tps.BAP_SetPrismType(value)

    def set_slope_distance(self, value):
        """

        :param value:
        :return:
        """
        "Schrägdistanz kann nicht gesetzt werden"

    def set_station(self, easting, northing, height, instrument_height):
        """

        :param easting: Rechtswert
        :type easting: float
        :param northing: Hochwert
        :type northing: float
        :param height: Höhe
        :type height: float
        :param instrument_height: Instrumentenhöhe
        :type instrument_height: float
        :return:
        """
        self.tps.TMC_SetStation(easting, northing, height, instrument_height)

    def set_stopbits(self, value):
        """

        :param value: Stopbits
        :type value: int
        :return:
        """
        self.tps.STOPBITS = value

    def get_stopbits(self):
        """

        :return:
        """
        return self.tps.STOPBITS

    def get_temperature(self):
        """

        :return:
        """
        return self.tps.CSV_GetIntTemp()["TEMPERATURE"]

    def get_baudrate(self):
        """

        :return:
        """
        return self.tps.BAUDRATE

    def get_bytesize(self):
        """

        :return:
        """
        return self.tps.BYTESIZE

    def get_parity(self):
        """

        :return:
        """
        return self.tps.PARITY

    def get_path(self):
        """

        :return:
        """
        return self.tps.PATH

    def switch_off(self):
        """

        :return:
        """
        self.tps.COM_SwitchOffTPS(eOffMode=MAIN.OFF)

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

    def get_angles(self, use_atr=True):
        """
        Liefert die aktuellen Stellwinkel beruecksichtigt dabei, ob ATR verwendet werden soll oder nicht

        :param use_atr: ATR
        :type use_atr: bool
        :return:
        """
        if use_atr:
            self.tps.AUT_FineAdjust()

        tmp = self.tps.TMC_GetAngle5()

        return tmp

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

        if 'SLOPE_DISTANCE' not in tmp:
            return {}

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

    def set_search_windows(self, search_horizontal, search_vertical):
        """
        Setze Suchfenster für Tachymeter
        :param search_horizontal: Suchbereich Horizontalkreis
        :type search_horizontal: float
        :param search_vertical: Suchbereich Vertikalkreis
        :type search_vertical: float
        :return:
        """
        self.__search_horizontal = search_horizontal
        self.__search_vertical = search_vertical

    def get_search_windows(self):
        """
        Liefert das Suchfesnter
        :return: SEARCH_HORIZONTAL, SEARCH_VERTICAL
        :rtype: dict
        """
        return {"SEARCH_HORIZONTAL": self.__search_horizontal,
                "SEARCH_VERTICAL": self.__search_vertical}

    def turn_to(self, horizontal_angle, vertical_angle):
        """

        :param horizontal_angle: Horizontalwinkel
        :type horizontal_angle: float
        :param vertical_angle: Vertikalwinkel
        :type vertical_angle: float
        :return:
        """
        self.tps.turn_to(horizontal_angle,
                         vertical_angle,
                         self.__search_horizontal,
                         self.__search_vertical)

    def measure(self):
        """

        :return: FACE, TEMPERATURE, HORIZONTAL_ANGLE, VERTICAL_ANGLE, SLOPE_DISTANCE, PPM, PRISM_CONSTAN, CROSS_INCLINE, LENGTH_INCLINE
        """
        #tmp = {'UID': GENERATES.gen_uuid(),
        #       'CREATED': GENERATES.gen_now(DATE_RETURN=True)}
        #tmp.update(self.get_face())
        #tmp.update(self.tps.BAP_MeasDistanceAngle(dist_mode=BAP.BAP_SINGLE_REF_VISIBLE))
        #return tmp
        return self.tps.measure(SEARCH_HORIZONTAL=self.__search_horizontal,
                                SEARCH_VERTICAL=self.__search_vertical,
                                FINE_ADJUST=True)

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
