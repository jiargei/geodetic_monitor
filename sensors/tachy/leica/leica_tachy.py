# -*- coding: utf-8 -*-

# Third Party Module Import
import time

# Package Import
from ..base import Tachy, ON, OFF
import tmc
import aut
import geocom
import logging
from common.utils import angle
from sensors import response


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
        return response.StateResponse(1)

    def clear(self):
        """

        :return:
        """
        self.communicate(geocom.COM_NullProc())
        self.communicate(geocom.TMC_DoMeasure(tmc.TMC_CLEAR))
        return response.Response()

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

    def get_slope_distance(self):
        """

        :return:
        """
        self.communicate(geocom.TMC_DoMeasure(tmc.TMC_CLEAR))
        self.communicate(geocom.TMC_DoMeasure(tmc.TMC_DEF_DIST))
        m = self.communicate(geocom.TMC_GetSimpleMea())
        return response.DistanceResponse(slope_distance=m["SLOPE_DISTANCE"],
                                         data_dict=m)

    def get_target(self):
        """

        :return:
        """
        d = self.communicate(geocom.TMC_GetCoordinate())
        return response.CoordinateResponse(easting=d["EASTING"],
                                           northing=d["northing"],
                                           height=d["height"],
                                           data_dict=d)

    def fine_adjust(self):
        """

        :return:
        """
        d = self.communicate(geocom.AUT_FineAdjust())
        return response.Response(data_dict=d)

    def get_response(self):
        """

        :return:
        """
        return response.Response(data_dict=self.communicate(geocom.COM_NullProc()))

    def set_reflector_height(self, value):
        return response.Response(data_dict=self.communicate(geocom.TMC_SetHeight(value)))

    def get_reflector_height(self):
        return response.Response(data_dict=self.communicate(geocom.TMC_GetHeight()))

    def set_station(self, easting, northing, height, instrument_height):
        return response.Response(data_dict=self.communicate(geocom.TMC_SetStation(easting,
                                                                                  northing,
                                                                                  height,
                                                                                  instrument_height)))

    def get_station(self):
        d = self.communicate(geocom.TMC_GetStation())
        return response.StationResponse(data_dict=d,
                                        instrument_height=d["INSTRUMENT_HEIGHT"],
                                        easting=d["EASTING"],
                                        northing=d["NORTHING"],
                                        height=d["HEIGHT"])

    def set_face(self, value):
        """

        :param value:
        :return:
        """
        assert value in [1, 0]
        current_face = self.get_face()["FACE"]
        current_face = int(current_face)
        logger.debug("FACE: %d" % current_face)
        cmd = {"status": response.RESPONSE_SUCCESS, "description": response.RESPONSE_DESCRIPTION}
        while int(value) != current_face:
            cmd = self.communicate(geocom.AUT_ChangeFace())
            current_face = int(self.get_face().state)
            logger.debug("FACE: %d" % current_face)
            time.sleep(1)
        return response.Response(data_dict=cmd)

    def get_face(self):
        d = self.communicate(geocom.TMC_GetFace())
        return response.StateResponse(data_dict=d,
                                      state=d["FACE"])

    def set_orientation(self, orientation):
        return response.Response(data_dict=self.communicate(geocom.TMC_SetOrientation(orientation)))

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

        d = self.communicate(geocom.AUT_MakePositioning(horizontal_angle=angle.gon2rad(hz),
                                                        vertical_angle=angle.gon2rad(v),
                                                        atr_mode=atr_mode))
        return response.Response(data_dict=d)

    def set_prism_constant(self, value):
        """

        :param value:
        :return:
        """
        return response.Response(data_dict=self.communicate(geocom.BAP_SetPrismType(prism_type=value)))

    def get_prism_constant(self):
        """

        :return:
        """
        d = self.communicate(geocom.TMC_GetPrismCorr())
        return response.FloatResponse(data_dict=d,
                                      value=d["PRISM_CONSTANT"])

    def get_temperature(self):
        """

        :return:
        """
        d = self.communicate(geocom.CSV_GetIntTemp())
        return response.TemperatureResponse(data_dict=d,
                                            temperature=d["INTERNAL_TEMPERATURE"])

    def switch_off(self):
        """

        :return:
        """
        return response.Response(data_dict=self.communicate(geocom.COM_SwitchOffTPS(on_off=ON)))

    def switch_on(self):
        """

        :return:
        """
        return response.Response(data_dict=self.communicate(geocom.COM_SwitchOffTPS(on_off=OFF)))

    def get_instrument_name(self):
        """

        :return:
        """
        d = self.communicate(geocom.CSV_GetInstrumentName())
        return response.StringResponse(data_dict=d,
                                       string=d["INSTRUMENT_NAME"])

    def get_instrument_number(self):
        """

        :return:
        """
        d = self.communicate(geocom.CSV_GetInstrumentNo())
        return response.StringResponse(data_dict=d,
                                       string=d['INSTRUMENT_NUMBER'])

    def get_angles(self, atr=True):
        """

        :param atr:
        :return:
        """
        if atr:
            self.communicate(geocom.AUT_FineAdjust(search_hz=self.search_hz,
                                                   search_v=self.search_v))

        get_angle = self.communicate(geocom.TMC_GetAngle5())

        return response.AngleResponse(horizontal_angle=angle.rad2gon(float(get_angle["HORIZONTAL_ANGLE"])),
                                      vertical_angle=angle.rad2gon(float(get_angle["VERTICAL_ANGLE"])),
                                      data_dict=get_angle)

    def get_search_windows(self):
        """

        :return:
        """
        return response.AngleResponse(horizontal_angle=self.search_hz,
                                      vertical_angle=self.search_v)

    def set_search_windows(self, search_horizontal, search_vertical):
        """

        :param search_horizontal:
        :param search_vertical:
        :return:
        """
        self.search_hz = search_horizontal
        self.search_v = search_vertical
        return response.Response()

    def connect(self):
        """

        :return:
        """
        if not self.connector.isOpen():
            self.connector.open()
        return response.Response()

    def get_compensator(self):
        """

        :return:
        """
        get_angle = self.communicate(geocom.TMC_GetAngle1())
        d = {
            "COMPENSATOR_CROSS": angle.rad2gon(float(get_angle["CROSS_INCLINE"])),
            "COMPENSATOR_LENGTH": angle.rad2gon(float(get_angle["LENGTH_INCLINE"])),
        }
        return response.CompensatorResponse(d["COMPENSATOR_CROSS"],
                                            d["COMPENSATOR_LENGTH"],
                                            data_dict=get_angle)

    def set_laser_pointer(self, value):
        """

        :param value:
        :return:
        """
        if value in [ON, OFF]:
            lp = self.communicate(geocom.EDM_SetLaserpointer(on_off=value))
            if lp["status"] == response.RESPONSE_SUCCESS:
                self.__laserpointer_state = value
        else:
            lp = {'status': response.RESPONSE_FAIL, 'description': 'Wrong Laserpointer state'}
            lp.update(self.get_laser_pointer())

        return response.Response(data_dict=lp)

    def set_instrument_modes(self, atr_mode, edm_mode, hz_tolerance, v_tolerance):
        """

        :param atr_mode:
        :param edm_mode:
        :param hz_tolerance:
        :param v_tolerance:
        :return:
        """
        # TODO ..
        return response.Response()

    def set_instrument_name(self, value):
        """
        NOT ALLOWED
        :param value:
        :return:
        """
        return response.Response(status=response.RESPONSE_WARN,
                                 description="setting name not allowed")

    def set_instrument_number(self, value):
        """
        NOT ALLOWED
        :param value:
        :return:
        """
        return response.Response(status=response.RESPONSE_WARN,
                                 description="setting snr not allowed")

    def get_ppm(self):
        m = self.communicate(geocom.TMC_GetSlopeDistCorr)
        return response.FloatResponse(value=m["PPM_CORR"],
                                      data_dict=m)
