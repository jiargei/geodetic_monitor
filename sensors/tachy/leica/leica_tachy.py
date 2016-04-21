# -*- coding: utf-8 -*-

# Third Party Module Import
import time

# Package Import
from ..base import Tachy, ON, OFF
import tmc
import aut
import geocom
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class LeicaTachy(Tachy):

    brand = "Leica Geosystems"

    @property
    def model_type(self):
        return "GeoCOM"

    def __init__(self, *args, **kwargs):
        """

        :param connector: serial.Serial
        :return:
        """
        super(LeicaTachy, self).__init__(*args, **kwargs)

    def is_leveled(self):
        """

        :return:
        """
        # TODO ..
        return True

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
        logger.debug("Write %s, %s" % (geocom_command.__class__, str(geocom_command)))
        logger.debug(geocom_command.GEOCOM_PARAMETERS)
        self.connector.write(str(geocom_command))
        geocom_command.set_serial_read(self.connector.readline())
        logger.debug("Got this: %s" % geocom_command.get_serial_read())

        return geocom_command.execute()

    def get_measurement(self):
        """

        :return:
        """
        self.communicate(geocom.TMC_DoMeasure(tmc.TMC_CLEAR))
        self.communicate(geocom.TMC_DoMeasure(tmc.TMC_DEF_DIST))
        return self.communicate(geocom.TMC_GetSimpleMea())

    def get_target(self):
        """

        :return:
        """
        d = self.communicate(geocom.TMC_GetCoordinate())
        d["EASTING"] = float(d["EASTING"])
        d["NORTHING"] = float(d["NORTHING"])
        d["HEIGHT"] = float(d["HEIGHT"])
        return d

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
        return self.communicate(geocom.TMC_SetStation(easting, northing, height, instrument_height))

    def get_station(self):
        return self.communicate(geocom.TMC_GetStation())

    def set_face(self, value):
        """

        :param value:
        :return:
        """
        assert value in [1, 0]
        current_face = self.get_face()["FACE"]
        current_face = int(current_face)
        logger.debug("FACE: %d" % current_face)
        while int(value) != current_face:
            cmd = self.communicate(geocom.AUT_ChangeFace())
            current_face = int(self.get_face()["FACE"])
            logger.debug("FACE: %d" % current_face)
            time.sleep(1)

    def get_face(self):
        return self.communicate(geocom.TMC_GetFace())

    def set_orientation(self, orientation):
        return self.communicate(geocom.TMC_SetOrientation(orientation))

    def set_angles(self, hz, v, atr):
        """

        :param hz:
        :param v:
        :param atr:
        :return:
        """
        if atr:
            atr_mode = aut.AUT_TARGET
        else:
            atr_mode = aut.AUT_POSITION
        return self.communicate(geocom.AUT_MakePositioning(horizontal_angle=hz,
                                                           vertical_angle=v,
                                                           atr_mode=atr_mode))

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

    def get_angles(self, use_atr=True):
        """

        :param use_atr:
        :return:
        """
        if use_atr:
            self.communicate(geocom.AUT_FineAdjust(search_hz=self.search_hz,
                                                   search_v=self.search_v))
        get_angle = self.communicate(geocom.TMC_GetAngle5())

        return get_angle

    def get_search_windows(self):
        """

        :return:
        """
        return {"SEARCH_HZ": self.search_hz,
                "SEARCH_V": self.search_v}

    def set_search_windows(self, search_horizontal, search_vertical):
        """

        :param search_horizontal:
        :param search_vertical:
        :return:
        """
        self.search_hz = search_horizontal
        self.search_v = search_vertical

    def connect(self):
        """

        :return:
        """
        if not self.connector.isOpen():
            self.connector.open()

    def get_compensator(self):
        """

        :return:
        """
        get_angle = self.communicate(geocom.TMC_GetAngle1())
        return {"COMPENSATOR_CROSS": get_angle["CROSS_INCLINE"],
                "COMPENSATOR_LENGTH": get_angle["LENGTH_INCLINE"]}

    def set_laser_pointer(self, value):
        """

        :param value:
        :return:
        """
        if value in [ON, OFF]:
            lp = self.communicate(geocom.EDM_SetLaserpointer(on_off=value))
            if lp["status"] == 200:
                self.__laserpointer_state = value

        else:
            lp = {'status': 409, 'description': 'Wrong Laserpointer state'}
            lp.update(self.get_laser_pointer())

        return lp

    def set_instrument_modes(self, atr_mode, edm_mode, hz_tolerance, v_tolerance):
        """

        :param atr_mode:
        :param edm_mode:
        :param hz_tolerance:
        :param v_tolerance:
        :return:
        """
        # TODO ..
        pass

    def set_instrument_name(self, value):
        """
        NOT ALLOWED
        :param value:
        :return:
        """
        pass

    def set_instrument_number(self, value):
        """
        NOT ALLOWED
        :param value:
        :return:
        """
        pass
