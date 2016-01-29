# -*- coding: utf-8 -*-

import re
from abc import ABCMeta, abstractproperty

import aut
import bap
import tmc
from returncodes import RETURNCODES
from sensors.tachy.hardware.tachy import ON

__author__ = 'jurgen'


def get_geocom_error(geocom_response):
    """

    :param geocom_response:
    :type geocom_response: int
    :return:
    """
    if geocom_response in RETURNCODES.keys():
        return "GeoCOM RETURNCODE: %s (%d)" % (RETURNCODES[geocom_response], geocom_response)


class GeoCOMCommand(object):
    __metaclass__ = ABCMeta

    GEOCOM_PREFIX = "%R1Q,"
    GEOCOM_SUFFIX = "\r\n"
    GEOCOM_REGEXP = r"((?P<geoCOMReplyType>\%R1P,)(?P<geoCOMReturnCode>\d))?((,)(?P<transactionID>\d))(:)(?P<returnCode>\d+)?(?P<parameters>.*)(\n)"

    def __str__(self):
        return "%s%s%s" % (self.GEOCOM_PREFIX, self.GEOCOM_QUERY, self.GEOCOM_SUFFIX)

    @abstractproperty
    def GEOCOM_QUERY(self):
        pass

    @abstractproperty
    def GEOCOM_PARAMETERS(self):
        return ['EMPTY']

    @classmethod
    def create_serial(cls):
        """
        Erzeugt String für Serial
        :return:
        :rtype: str
        """
        return "%s%s%s" % (cls.GEOCOM_PREFIX, cls.GEOCOM_QUERY, cls.GEOCOM_SUFFIX)

    def set_serial_read(self, serial_read):
        self.serial_read = serial_read

    @classmethod
    def is_valid_geocom_regexp(cls, serial_response):
        """
        Prüft, ob der String von Serial dem GeoCOM Muster entspricht
        :param serial_response:
        :return: True, wenn der SerialString dem GeoCOM Muster entspricht, sonst False
        :rtype: bool
        """
        regexp = re.search(cls.GEOCOM_REGEXP, serial_response)
        return regexp is not None

    @staticmethod
    def is_valid_geocom_response(geocom_returncode):
        """
        Prüft, ob der GeoCOM Returncode gültig ist
        :param geocom_returncode:
        :return: True, wenn der Returncode OK ist, sonst False
        :rtype: bool
        """
        return geocom_returncode in [0]

    @classmethod
    def is_valid_parameters_length(cls, parameters_list):
        """
        Prüft, ob Anzahl der Parameter der Klasse gleich parameters_list
        :param parameters_list:
        :return: True, wenn Anzahl der Elemente gleich, sonst False
        :rtype: bool
        """
        # print (cls.GEOCOM_PARAMETERS)
        # print (parameters_list)

        return len(cls.GEOCOM_PARAMETERS) == len(parameters_list)

    def get_parameters(self, serial_parameters):
        """
        Zerlegt die Parameter von Serial und erzeugt ein dict
        :param serial_parameters:
        :return: PARAMETERS
        :rtype: dict
        """
        parameter_dict = {'status': 409, 'description': 'Conflict - wrong numbers of parameters'}

        if self.is_valid_parameters_length(serial_parameters):
            for i in range(len(self.GEOCOM_PARAMETERS)):
                parameter_dict.update({self.GEOCOM_PARAMETERS[i]: serial_parameters[i]})
            parameter_dict['status'] = 200
            parameter_dict['description'] = 'OK'

        return parameter_dict

    def execute(self):
        """
        Ausführen eines GeoCOM Commandos
        :return:
        """
        return self.geocom_check(self.serial_read)

    def geocom_check(self, serial_read):
        serial_read = serial_read.replace("\r", "")

        # Prüfe ob GeoCOM REGEX Pattern entspricht
        if self.is_valid_geocom_regexp(serial_read):
            regexp = re.search(self.GEOCOM_REGEXP, serial_read)
            geocom_returncode = int(regexp.group("returnCode"))

            # Prüfe, ob GeoCOM Returncode passt
            if self.is_valid_geocom_response(geocom_returncode):
                geocom_parameters = regexp.group("parameters")[1:]
                geocom_parameters = geocom_parameters.split(',')

                # Liefere GeoCOM Return-Parameter
                return self.get_parameters(geocom_parameters)
            else:
                return {'status': 412, 'description': get_geocom_error(geocom_returncode)}
        else:
            return {'status': 400, 'descritption': 'GeoCOM regexp did not match'}


class COM_NullProc(GeoCOMCommand):
    """
    ASCII-Request: %R1Q,0:\n
    ASCII-Response: %R1P,0,0:RC\n
    Remarks: \n
    This function does not provide any functionality except of checking if the communication is up and running.
    """
    @property
    def GEOCOM_QUERY(self):
        return "0:"

    GEOCOM_PARAMETERS = ['EMPTY']


class TMC_GetAngle1(GeoCOMCommand):
    """
    ASCII-Request: %R1Q,2003:Mode[long]\n
    ASCII-Response: %R1P,0,0:RC,Hz[double],V[double],AngleAccuracy[double],
    AngleTime[long],CrossIncline[double],LengthIncline[double], AccuracyIncline[double],InclineTime[long],FaceDef[long]
    Remarks:\n
    This function carries out an angle measurement and, in dependence of configuration, inclination measurement
    and returns the results. As shown the result is very comprehensive. For simple angle measurements use
    TMC_GetAngle5 or TMC_GetSimpleMea instead.
    Information about measurement is returned in the return code.
    """

    def __init__(self, inclination_mode=tmc.TMC_MEA_INC):
        self.__inclination_mode = inclination_mode

    def set_inclination_mode(self, value):
        if value in [0, 1, 2]:
            self.__inclination_mode = value
        else:
            self.__inclination_mode = 1

    @property
    def GEOCOM_QUERY(self):
        return "2003:%d" % self.__inclination_mode

    GEOCOM_PARAMETERS = ['HORIZONTAL_ANGLE', 'VERTICAL_ANGLE',
                         'ANGLE_ACCURACY', 'ANGLE_TIME',
                         'CROSS_INCLINE', 'LENGTH_INCLINE',
                         'ACCURACY_INCLINE', 'INCLINE_TIME',
                         'FACE_DEF']


class TMC_DoMeasure(GeoCOMCommand):
    """
    ASCII-Request: %R1Q,2008:Command[long],Mode[long]\n
    ASCII-Response: %R1P,0,0:RC\n
    Remarks:\n
    This function carries out a distance measurement according to the TMC measurement mode like single distance,
    tracking,... . Please note that this command does not output any values (distances). In order to get the values you
    have to use other measurement functions such as TMC_GetCoordinate, TMC_GetSimpleMea or TMC_GetAngle.
    The result of the distance measurement is kept in the instrument and is valid to the next TMC_DoMeasure command
    where a new distance is requested or the distance is clear by the measurement program TMC_CLEAR.
    """

    def __init__(self, measurement_mode=tmc.TMC_DEF_DIST, inclination_mode=tmc.TMC_MEA_INC):
        self.__inclination_mode = inclination_mode
        self.__measurement_mode = measurement_mode

    def set_inclination_mode(self, value):
        if value in [0, 1, 2]:
            self.__inclination_mode = value
        else:
            self.__inclination_mode = 1

    def set_measurement_mode(self, value):
        if value in [0, 1, 3, 4, 6, 8, 10, 11]:
            self.__measurement_mode = value
        else:
            self.__measurement_mode = tmc.TMC_DEF_DIST

    @property
    def GEOCOM_QUERY(self):
        return "2008:%d,%d" % (self.__measurement_mode, self.__inclination_mode)

    GEOCOM_PARAMETERS = ['EMPTY']


class TMC_GetStation(GeoCOMCommand):
    """
    ASCII-Request: %R1Q,2009:\n
    ASCII-Response: %R1P,0,0:RC,E0[double],N0[double],H0[double],Hi[double]\n
    Remarks:\n
    This function is used to get the station coordinates of the instrument.
    """

    @property
    def GEOCOM_QUERY(self):
        return "2009:"

    GEOCOM_PARAMETERS = ['EASTING', 'NORTHING', 'HEIGHT', 'INSTRUMENT_HEIGHT']


class TMC_SetStation(GeoCOMCommand):
    """
    ASCII-Request: %R1Q,2010:E0[double],N0[double],H0[double],Hi[double]\n
    ASCII-Response: %R1P,0,0:RC\n
    Remarks:\n
    This function is used to set the station coordinates of the instrument.
    """

    def __init__(self, easting, northing, height, instrument_height):
        self.__easting = easting
        self.__northing = northing
        self.__height = height
        self.__instrument_height = instrument_height

    @property
    def GEOCOM_QUERY(self):
        return "2010:%f,%f,%f,%f" % (self.__easting, self.__northing, self.__height, self.__instrument_height)

    GEOCOM_PARAMETERS = ['EMPTY']


class TMC_GetHeight(GeoCOMCommand):
    """
    ASCII-Request: %R1Q,2011:\n
    ASCII-Response: %R1P,0,0:RC,Height[double]\n
    Remarks:\n
    This function returns the current reflector height.
    """

    @property
    def GEOCOM_QUERY(self):
        return "2011:"

    GEOCOM_PARAMETERS = ['REFLECTOR_HEIGHT']


class TMC_SetHeight(GeoCOMCommand):
    """
    ASCII-Request: %R1Q,2012:Height[double]\n
    ASCII-Response: %R1P,0,0:RC\n
    Remarks:\n
    This function sets a new reflector height.
    """

    def __init__(self, reflector_height=0.0):
        self.__reflector_height = reflector_height

    @property
    def GEOCOM_QUERY(self):
        return "2012:%f" % self.__reflector_height

    GEOCOM_PARAMETERS = ['EMPTY']


class TMC_SetEdmMode(GeoCOMCommand):
    """
    ASCII-Request: %R1Q,2020:Mode[long]\n
    ASCII-Response: %R1P,0,0:RC\n
    Remarks:\n
    This function sets the current measurement mode. The measure function TMC_DoMeasure(TMC_DEF_DIST)
    uses this configuration.

    EDM_MODE_NOT_USED = 0   # Init value
    EDM_SINGLE_TAPE = 1     # IR Standard Reflector Tape
    EDM_SINGLE_STANDARD = 2 # IR Standard
    EDM_SINGLE_FAST = 3     # IR Fast
    EDM_SINGLE_LRANGE = 4   # LO Standard
    EDM_SINGLE_SRANGE = 5   # RL Standard
    EDM_CONT_STANDARD = 6   # Standard repeated measurement
    EDM_CONT_DYNAMIC = 7    # IR Tracking
    EDM_CONT_REFLESS = 8    # RL Tracking
    EDM_CONT_FAST = 9       # Fast repeated measurement
    EDM_AVERAGE_IR = 10     # IR Average
    EDM_AVERAGE_SR = 11     # RL Average
    EDM_AVERAGE_LR = 12     # LO Average
    """

    def __init__(self, edm_measurement_mode):
        self.__edm_measurement_mode = edm_measurement_mode

    @property
    def GEOCOM_QUERY(self):
        return "2020:%d" % self.__edm_measurement_mode

    GEOCOM_PARAMETERS = ['EMPTY']


class TMC_GetPrismCorr(GeoCOMCommand):
    """
    ASCII-Request: %R1Q,2023:\n
    ASCII-Response: %R1P,0,0:RC,PrismCorr[double]\n
    Remarks:\n
    This function is used to get the prism constant.
    :return:
    """

    @property
    def GEOCOM_QUERY(self):
        return "2023:"

    GEOCOM_PARAMETERS = ['PRISM_CORR']


class TMC_GetFace(GeoCOMCommand):
    """
    ASCII-Request: %R1Q,2026:\n
    ASCII-Response: %R1P,0,0:RC,Face[long]\n
    Remarks:\n
    This function returns the face information of the current telescope position. The face information is only valid, if
    the instrument is in an active measurement state (that means a measurement function was called before the
    TMC_GetFace call, see example). Note that the instrument automatically turns into an inactive measurement
    state after a predefined timeout.
    """

    @property
    def GEOCOM_QUERY(self):
        return "2026:"

    GEOCOM_PARAMETERS = ['FACE']


class TMC_SetOrientation(GeoCOMCommand):
    """
    ASCII-Request: %R1Q,2113:HzOrientation[double]\n
    ASCII-Response: %R1P,0,0:RC\n
    Remarks:\n
    This function is used to orientate the instrument in Hz direction. It is a combination of an angle measurement to
    get the Hz offset and afterwards setting the angle Hz offset in order to orientates onto a target. Before the new
    orientation can be set an existing distance must be cleared (use TMC_DoMeasure with the command =
    TMC_CLEAR).
    """

    def __init__(self, orientation):
        self.__orientation = orientation

    @property
    def GEOCOM_QUERY(self):
        return "2113:%f" % self.__orientation

    GEOCOM_PARAMETERS = ['EMPTY']


class AUT_ChangeFace(GeoCOMCommand):
    """
    ASCII-Request: %R1Q,9028:PosMode,ATRMode,0\n
    ASCII-Response: %R1P,0,0:RC\n
    Remarks:\n
    This procedure turns the telescope to the other face. If another function is active, for example locking onto a
    target, then this function is terminated and the procedure is executed.
    If the position mode is set to normal (PosMode = AUT_NORMAL) it is allowed that the current value of the
    compensator measurement is inexact. Positioning precise (PosMode = AUT_PRECISE) forces a new
    compensator measurement. If this measurement is not possible, the position does not take place.
    If ATR mode is activated and the ATR mode is set to AUT_TARGET, the instrument tries to position onto a target
    in the destination area.
    If LOCK mode is activated and the ATR mode is set to AUT_TARGET, the instrument tries to lock onto a target
    in the destination area.
    """

    def __init__(self, position_mode=aut.AUT_PRECISE, atr_mode=aut.AUT_POSITION):
        self.__position_mode = position_mode
        self.__atr_mode = atr_mode

    @property
    def GEOCOM_QUERY(self):
        return "9028:%d,%d" % (self.__position_mode, self.__atr_mode)

    GEOCOM_PARAMETERS = ['EMPTY']


class AUT_MakePositioning(GeoCOMCommand):
    """
    ASCII-Request: %R1Q,9027:Hz,V,PosMode,ATRMode,0\n
    ASCII-Response: %R1P,0,0:RC\n
    Remarks:\n
    This procedure turns the telescope absolute to the in Hz and V specified position, taking tolerance settings for
    positioning (see AUT_POSTOL) into account. Any active control function is terminated by this function call.
    If the position mode is set to normal (PosMode = AUT_NORMAL) it is assumed that the current value of the
    compensator measurement is valid. Positioning precise (PosMode = AUT_PRECISE) forces a new compensator
    measurement at the specified position and includes this information for positioning.
    If ATR mode is activated and the ATR mode is set to AUT_TARGET, the instrument tries to position onto a target
    in the destination area.
    If LOCK mode is activated and the ATR mode is set to AUT_TARGET, the instrument tries to lock onto a target
    in the destination area.
    """

    def __init__(self, horizontal_angle=0.0, vertical_angle=100.0,
                 position_mode=aut.AUT_PRECISE,
                 atr_mode=aut.AUT_POSITION):
        self.__horizontal_angle = horizontal_angle
        self.__vertical_angle = vertical_angle
        self.__position_mode = position_mode
        self.__atr_mode = atr_mode

    @property
    def GEOCOM_QUERY(self):
        return "9027:%f,%f,%d,%d,0" % (self.__horizontal_angle,
                                       self.__vertical_angle,
                                       self.__position_mode,
                                       self.__atr_mode)

    GEOCOM_PARAMETERS = ['EMPTY']


class BAP_SetPrismType(GeoCOMCommand):
    """
    ASCII-Request: %R1Q,17008: ePrismType [long]\n
    ASCII-Response: %R1P,0,0:RC\n
    Remarks:\n
    Sets the prism type for measurements with a reflector. It overwrites the prism constant, set by
    TMC_SetPrismCorr.

    :type   PrismType           : int
    :param  PrismType           : Prism Type (default = 1)
    """

    def __init__(self, prism_type=bap.BAP_PRISM_MINI):
        self.__prism_type = prism_type

    @property
    def GEOCOM_QUERY(self):
        return "17008:%d" % self.__prism_type

    GEOCOM_PARAMETERS = ['EMPTY']


class EDM_SetLaserpointer(GeoCOMCommand):

    def __init__(self, on_off=ON):
        self.__on_off = on_off

    @property
    def GEOCOM_QUERY(self):
        return "10004:%d" % self.__on_off


class AUT_FineAdjust(GeoCOMCommand):
    """
    ASCII-Request: %R1Q,9037:dSrchHz[double], dSrchV[double],0\n
    ASCII-Response: %R1P,0,0:RC\n
    Remarks:\n
    This procedure precisely positions the telescope crosshairs onto the target prism and measures the ATR Hz and
    V deviations. If the target is not within the visible area of the ATR sensor (Field of View) a target search will be
    executed. The target search range is limited by the parameter dSrchV in V- direction and by parameter dSrchHz
    in Hz - direction. If no target found the instrument turns back to the initial start position.
    A current Fine Adjust LockIn towards a target is terminated by this procedure call. After positioning, the lock
    mode is active. The timeout of this operation is set to 5s, regardless of the general position timeout settings. The
    positioning tolerance is depends on the previously set up the fine adjust mode (see AUT_SetFineAdjustMoed
    and AUT_GetFineAdjustMode).
    Tolerance settings (with AUT_SetTol and AUT_ReadTol) have no influence to this operation. The tolerance
    settings as well as the ATR measure precision depends on the instrument’s class and the used EDM measure
    mode (The EDM measure modes are handled by the subsystem TMC).
    """

    def __init__(self, search_hz=0.0100, search_v=0.0100):
        self.__search_horizontal = search_hz
        self.__search_vertical = search_v

    @property
    def GEOCOM_QUERY(self):
        return "9037:%f,%f,0" % (self.__search_horizontal, self.__search_vertical)

    GEOCOM_PARAMETERS = ['EMPTY']


class CSV_GetIntTemp(GeoCOMCommand):
    """
    ASCII-Request: %R1Q,5011:\n
    ASCII-Response: %R1P,0,0:RC,Temp[long]\n
    Remarks:\n
    Get the internal temperature of the instrument, measured on the Mainboard side. Values are reported in degrees
    Celsius.

    :rtype: dict
    :return: TEMPERATURE
    """

    @property
    def GEOCOM_QUERY(self):
        return "5011:"

    GEOCOM_PARAMETERS = ['INTERNAL_TEMPERATURE']


class COM_SwitchOffTPS(GeoCOMCommand):
    """
    ASCII-Request: %R1Q,112:eOffMode[short]\n
    ASCII-Response: %R1P,0,0:RC\n
    Remarks: This function switches off the TPS1200 instrument.

    :rtype: `bool <https://docs.python.org/2/library/functions.html#bool>`_
    :return: If query succeeded or not
    """

    def __init__(self, on_off=NO):
        self.__on_off = on_off

    @property
    def GEOCOM_QUERY(self):
        return "112:%d" % self.__on_off

    GEOCOM_PARAMETERS = ['EMPTY']


class CSV_GetInstrumentNo(GeoCOMCommand):
    """
    ASCII-Request: %R1Q,5003:\n
    ASCII-Response: %R1P,0,0:RC, SerialNo[long]\n
    Remarks:\n
    Gets the factory defined serial number of the instrument.
    """

    @property
    def GEOCOM_QUERY(self):
        return "5003:"

    GEOCOM_PROPERTIES = ['INSTRUMENT_NUMBER']


class CSV_GetInstrumentName(GeoCOMCommand):
    """
    ASCII-Request: %R1Q,5004:\n
    ASCII-Response: %R1P,0,0:RC,Name[string]\n
    Remarks:\n
    Gets the instrument name, for example: TCRP1201 R300

    :rtype: dict
    :return: INSTRUMENT_NAME
    """

    @property
    def GEOCOM_QUERY(self):
        return "5004:"

    GEOCOM_PROPERTIES = ["INSTRUMENT_NAME"]
