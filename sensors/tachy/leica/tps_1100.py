# -*- coding: utf-8 -*-

# Third Party Module Import
import time

# Package Import
from leica_tachy import LeicaTachy
from sensors.tachy.leica import geocom
from sensors.tachy import base
from sensors.tachy.leica import tmc
from sensors.tachy.leica import bap
# from dimosy import VARS
# from dimosy import TOOLS
# from dimosy.TOOLS import GENERATES


class TPS1100(LeicaTachy):
    """

    """

    model = "TPS1100"

    def __init__(self, tps):
        """

        :param tps:
        :type tps: ??  # TODO
        :return:
        """
        self.tps = tps
        super(TPS1100, self).__init__()

    def get_model_id(self):
        return 11

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

    def set_slope_distance(self, value):
        """

        :param value:
        :return:
        """
        "Schrägdistanz kann nicht gesetzt werden"

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

    @staticmethod
    def get_tachymeter_type():
        return {"TACHYMETER_TYPE": "Leica Tachymeter"}

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

    def get_angles(self, atr):
        """
        Liefert die aktuellen Stellwinkel beruecksichtigt dabei, ob ATR verwendet werden soll oder nicht

        :param atr: ATR
        :type atr: bool
        :return:
        """
        if atr:
            self.tps.AUT_FineAdjust()

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

        assert value in [base.ON, base.OFF]
        if value == base.ON:
            tmp = self.tps.EDM_Laserpointer_ON()

        elif value == base.OFF:
            tmp = self.tps.EDM_Laserpointer_OFF()

        self.__laserpointer = value
        return {"RESULT": tmp}


    def get_slope_distance(self):
        """
        Liefert die gemessene Schraegstecke
        :return:
        """
        setter_dict = ["self.TMC_DoMeasure(TMC.TMC_CLEAR, EDM.EDM_SINGLE_TAPE)",
                       "self.TMC_DoMeasure(%d, %d)" % (tmc.TMC_DEF_DIST, tmc.TMC_AUTO_INC)]

        getter_dict = ["self.TMC_GetSimpleMea(%d, %d)" % (base.WAIT_TIME, tmc.TMC_AUTO_INC),
                       "self.TMC_DoMeasure(TMC.TMC_CLEAR, EDM.EDM_SINGLE_TABE"]

        tmp = self.tps.do_dict(setter_dict=setter_dict,
                               getter_dict=getter_dict,
                               command_retry=base.COMMAND_RETRIES,
                               command_wait=base.COMMAND_WAIT)

        return {"SLOPE_DISTANCE": tmp["SLOPE_DISTANCE"]}



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

    def get_measurement(self):
        """

        :return: FACE, TEMPERATURE, HORIZONTAL_ANGLE, VERTICAL_ANGLE, SLOPE_DISTANCE, PPM, PRISM_CONSTAN, CROSS_INCLINE, LENGTH_INCLINE
        """
        #tmp = {'UID': GENERATES.gen_uuid(),
        #       'CREATED': GENERATES.gen_now(DATE_RETURN=True)}
        #tmp.update(self.get_face())
        #tmp.update(self.tps.BAP_MeasDistanceAngle(dist_mode=BAP.BAP_SINGLE_REF_VISIBLE))
        #return tmp
        return self.tps.get_measurement(SEARCH_HORIZONTAL=self.__search_horizontal,
                                        SEARCH_VERTICAL=self.__search_vertical,
                                        FINE_ADJUST=True)

    def connect(self):
        """

        :return:
        """
        # Versuche wiederholt, mit dem Tachymeter Kontakt herzustellen
        try_to_connect = 0
        while not self.tps.COM_NullProc() and try_to_connect <= base.NULL_PRO_RETRY_ATTEMP:
            time.sleep(base.NULL_PRO_RETRY_TIME)
            try_to_connect += 1
        return self.tps.COM_NullProc()

    def is_leveled(self):
        """
        Prüft, ob das Gerät horizontiert ist.

        :return: True, wenn der Tachymeter horizontiert ist, sonst False
        :rtype: bool
        """
        return self.tps.is_horizonted()
