# -*- coding: utf-8 -*-

# external packages
import time
import re
import sys
import math

from serial import serialutil

# internal packages
from ..sensors import CON, ERROR

from ..constants import MAIN
from ..tools import ANGLE, GENERATES

from . import GEOCOM_RETURNCODES
from . import TMC, EDM, BAP, AUT, MOT


def GeoCOMError(QUERY, REQUEST):
    sys.stdout.write("@ %s%s\n" % (QUERY, REQUEST))
    sys.stdout.flush()


class ErrorGeoComReturnCode(Exception):

    def __init__(self, RC_VALUE):
        self.RC_VALUE = RC_VALUE
        self.RC_NAME = GEOCOM_RETURNCODES.ReturnCodeDict[self.RC_VALUE]
        sys.stdout.write("GeoCOM RC Error: RC_Value: %d, RC_Name: %s" % (self.RC_VALUE, self.RC_NAME))
        sys.stdout.flush()


class ErrorWithArgs(Exception):

    def __init__(self, *args):
        # *args is used to get a list of the parameters passed in
        #self.args = [a for a in args]
        self.WHERE = args[0]
        self.WHAT = args[1]
        self.PRINT = args[2]
        if self.PRINT:
            sys.stdout.write("@ %s%s" % (self.WHERE, self.WHAT))
            sys.stdout.flush()

        # print "GeoCOM Error: %s"%a[0]


class GeoCOM(CON.Con):
    """
    Communication Class for TPS
    """

    def __init__(self,
                 BAUDRATE=9600,
                 STOPBITS=1,
                 BYTESIZE=8,
                 PATH=None,
                 PARITY='N',
                 RTSCTS=0,
                 TIMEOUT=15,
                 WRITE_TIMEOUT=15,
                 XONXOFF=0,
                 WAIT_MEASURE=0.001,
                 MODEL_ID=15):

        CON.Con.__init__(self,
                                BAUDRATE=BAUDRATE,
                                STOPBITS=STOPBITS,
                                BYTESIZE=BYTESIZE,
                                PATH=PATH,
                                PARITY=PARITY,
                                RTSCTS=RTSCTS,
                                TIMEOUT=TIMEOUT,
                                WRITE_TIMEOUT=WRITE_TIMEOUT,
                                XONXOFF=XONXOFF,
                                WAIT_MEASURE=WAIT_MEASURE)

        self.line_end = "\r\n"
        self.PARAMETER = ""
        self.RETURNCODE = "-1"
        self.connect()
        self.OUT = ""
        self.TIMEOUT = 15

    @staticmethod
    def config(SCREEN="desktop"):
        """

        :param SCREEN: Optimierung der Ausgabe für Desktop oder Mobilgerät
        :type SCREEN: str
        :return:
        """
        if SCREEN == "desktop":
            print """
                    #####################################################
                    ##              WICHTIGER HINWEIS                  ##
                    ##                                                 ##
                    ## Damit DiMoSy deine Sensoren finden kann,        ##
                    ## müssen diese ordnungsgemäß konfiguriert sein.   ##
                    ##                                                 ##
                    ##-------------------------------------------------##
                    ## Für einen Tachymeter der Firma Leica T1x        ##
                    ## führe bitte folgendes duch:                     ##
                    ##                                                 ##
                    ## 1)  Gerät einschalten                           ##
                    ## 2)  Sicherstellen, dass es horizontiert ist     ##
                    ## 3)  Im Hauptmenü                                ##
                    ## 4)  Wähle [5] 'Konfiguration'                   ##
                    ## 5)  Anschließend [1] 'Instrumentkonfig.'        ##
                    ## 6)  Anschließend [04] 'Auto Ein/Aus'            ##
                    ## 7)  Wähle "Autostart" --> Hauptmenü             ##
                    ## 8)  Wähle "Power Mode" --> Permanent EIN        ##
                    ## 9)  Zurück ins Konfigurationsmenü (2x [F1])     ##
                    ## 10) Wähle [2] Kommunikation                     ##
                    ## 11) Wähle [2] GeoCOM Parameter                  ##
                    ## 12) Setze Baudrate zu 9600                      ##
                    ## 13) Wechsle zu Kommunikation [F1]               ##
                    ## 14) Wähle [3] GeoCOM On-Line mode               ##
                    ## 15) Wähle [F4] JA.                              ##
                    ## 16) GeoCOM MUSS eingeschalten bleiben! Bitte    ##
                    ##     NICHT auf ENDE drücken!                     ##
                    ##                                                 ##
                    ## Das Gerät sollte nun einsatzbereit sein.        ##
                    ## Sollten dennoch Verbindungsfehler auftreten,    ##
                    ## versichere dich, dass das Gerät eingeschalten,  ##
                    ## die Stromversorgung sichergestellt und eine     ##
                    ## Verbindung zwischen Koffer und Gerät            ##
                    ## hergestellt ist.                                ##
                    ##                                                 ##
                    ## Ansonsten wende dich an die DiMoSy-Mitarbeiter  ##
                    ##                                                 ##
                    #####################################################
        """
        if SCREEN == "mobile":
            print u"Bitte das Gerät zur Verwendung mit"
            print u"GeoCOM konfigurieren. Bei Fragen wende"
            print u"dich an die DiMoSy-Mitarbeiter!"

    def help(self):
        self.getCommandList()

    def getCommandList(self):
        """
        Returniert eine Ausgabe aller implementierten Befehle

        :return: Liste aller Befehle
        :rtype: str
        """
        answer = """
dimosy.TACHY.TPS.GeoCOM()
======================
* COM *
    COM_NullProc()
    COM_SwitchOnTPS()
    COM_SwitchOffTPS( eOffMode=0 )
* EDM *
    EDM_Laserpointer_ON()
    EDM_Laserpointer_OFF()
* TMC *
    TMC_GetAngle1( INC_Mode )
    TMC_DoMeasure( TMC_Mode, EDM_Mode )
    TMC_GetStation()
    TMC_SetStation( E0, N0, H0, iH0 )
    TMC_GetHeight()
    TMC_SetHeight( REFLECTOR_HEIGHT )
    TMC_SetEdmMode( EDM_Mode )
    TMC_GetFace()
    TMC_SetAtmCorr( Lambda, Pressure, DryTemperature, WetTemperature )
    TMC_GetAngle5( INC_Mode )
    TMC_GetSimpleMea( INC_Mode )
    TMC_SetOrientation( HzOrientation )
    TMC_GetSimpleCoord( INC_Mode )
    TMC_QuickDist()
    TMC_GetSlopeDistCorr()
* CSV *
    CSV_GetInstrumentNo()
    CSV_GetInstrumentName()
    CSV_GetIntTemp()
* AUT *
    AUT_SetTol( ToleranceHz, ToleranceV )
    AUT_LockIn()
    AUT_MakePositioning( Hz, V, PosMode, ATRMode )
    AUT_ChangeFace()
    AUT_FineAdjust( dSrchHz, dSrchV )
    AUT_GetUserSpiral()
    AUT_SetUserSpiral( DRANGE_HZ, DRANGE_V )
* BAP *
    BAP_SetPrismType( PrismType )
    BAP_GetPrismType()
    BAP_MeasDistanceAngle( DistMode )
* AUS *
    AUS_SetUserAtrState( OnOff )
    AUS_GetUserAtrState()
    AUS_SetUserLockState( OnOff )
    AUS_GetUserLockState()
* MOT *
    MOT_StopController( mode )
    MOT_StartController( ControlMode )
    MOT_SetVelocity( HZ_Speed, V_Speed ) """
        print answer
        return answer

    def clearParameter(self):
        self.PARAMETER = None

    def is_type(self):
        """Prueft ob es sich um einen TPS-Sensor handelt"""
        try:
            # if self.query("5003:",USE_READLINE=False,SIGNAL_DELAY=1,SLEEP=0.5):
            #if self.TMC_GetFace(SHOW_ERROR=False, SIGNAL_DELAY=1, SLEEP=0):
            if self.COM_NullProc():
                return True
            else:
                return False
        except:  # ErrorWithArgs:
            # print "Keine Verbindung zu TPS"
            return False

    def single_query(self,
                     QUERY_STRING='2008:%d' % TMC.TMC_CLEAR,
                     SLEEP=0.0,
                     SHOW_ERROR=False,
                     SER_READ=10,
                     ERROR_HANDLER1=True,
                     SIGNAL_DELAY=None,
                     USE_READLINE=True,
                     ALLOW_UNSTABLE=False):
        # print "def single_query()"
        return self.single_query2(QUERY_STRING=QUERY_STRING,
                                  SHOW_ERROR=SHOW_ERROR,
                                  ALLOW_UNSTABLE=ALLOW_UNSTABLE)

    def single_query2(self, QUERY_STRING="2008:3", SHOW_ERROR=False, ALLOW_UNSTABLE=False):
        return self.query2(query_string=QUERY_STRING,
                           show_error=SHOW_ERROR,
                           allow_unstable=ALLOW_UNSTABLE)

    def single_query1(self,
                      QUERY_STRING='2008:%d' % TMC.TMC_CLEAR,
                      SLEEP=0.0,
                      SHOW_ERROR=False,
                      SER_READ=10,
                      ERROR_HANDLER1=True,
                      SIGNAL_DELAY=None,
                      USE_READLINE=True,
                      ALLOW_UNSTABLE=False):
        """
        Schickt ein Kommando QUERY_STRING an den Tachymeter und ladet die Antwort self.OUT in die Instanz.
        :rtype: `bool <https://docs.python.org/2/library/functions.html#bool>`_
        :return: liefert True, wenn ein Kommando an den Tachymeter gesendet werden konnte, sonst False
        """

        use_readline = True  # if self.USE_READLINE == 1 else False

        if SIGNAL_DELAY and SIGNAL_DELAY > self.TIMEOUT:
            self.TIMEOUT = SIGNAL_DELAY

        if SLEEP and SLEEP > self.TIMEOUT:
            self.TIMEOUT = SLEEP

        "Serielle Schnittstelle bereinigen"
        self.check_open()
        self.SERIAL.flush(); self.SERIAL.flushInput(); self.SERIAL.flushOutput()
        self.SERIAL.write("%R1Q," + QUERY_STRING + "\r\n")
        break_sign = re.compile("\r\n")

        "Serielle Schnittstelle auslesen"

        t_out = ""
        start_time = time.time()
        delta_time = 0

        # Suche nach "\r\n" in GeoCOM Output
        try:

            while (delta_time < self.TIMEOUT) and (not break_sign.search(t_out)):
                t_out += self.SERIAL.readline() if USE_READLINE else self.SERIAL.read(SER_READ)
                delta_time = time.time() - start_time

        except serialutil.SerialException:
            print self.SERIAL.inWaiting()

        "Suche nach korrekten GeoCOM Output"

        m = re.search(r"((?P<geoCOMReplyType>\%R1P,)(?P<geoCOMReturnCode>\d))?((,)(?P<transactionID>\d))(:)(?P<returnCode>\d+)?(?P<parameter>.*)(\n)", t_out)

        "Lese GeoCOM Output"

        if m is not None:
            # print "m: ", m.groupdict()
            self.OUT = t_out.replace("\n", "").replace("\r", "")
            self.RETURNCODE = m.group("returnCode")
            self.ERRORCODE = ""
            self.PARAMETER = m.group("parameter")[1:]
            #_ERROR_BOOL = False
        else:
            self.RETURNCODE = "-1"
            self.ERRORCODE = "Incorrect TPS output for query %s" % QUERY_STRING
            #_ERROR_BOOL = False

        "Bewertung von GeoCOM Output"

        if self.RETURNCODE == "0":
            _ERROR_BOOL = True
        elif ALLOW_UNSTABLE and self.RETURNCODE == "1284":
            _ERROR_BOOL = True
        elif int(self.RETURNCODE) in GEOCOM_RETURNCODES.ReturnCodeDict:
            _ERROR_BOOL = False
            if SHOW_ERROR:
                GeoCOMError("GeoCOM::Q %-10s... " % QUERY_STRING[:10], "::R %-6s" % str(self.RETURNCODE)[:6])
            #raise ErrorWithArgs("GeoCOM::Q %-9s... "%QUERY_STRING[:10], "::R %-7s"%str(self.RETURNCODE)[:6], ERROR_HANDLER1)
        else:
            _ERROR_BOOL = False
            if SHOW_ERROR:
                GeoCOMError("GeoCOM::Q %-5s... " % QUERY_STRING[:5], "::%-13s" % "UNBEKANNT")
            #raise ErrorWithArgs("GeoCOM::Q %-9s... "%QUERY_STRING[:10], "::%9s" % "UNBEKANNT", ERROR_HANDLER1)
        return _ERROR_BOOL

    def query(self,
              QUERY_STRING='2008:%d' % TMC.TMC_CLEAR,
              SLEEP=0.0,
              SHOW_ERROR=True,
              SER_READ=10,
              ERROR_HANDLER1=True,
              SIGNAL_DELAY=None,
              USE_READLINE=True,
              ALLOW_UNSTABLE=False):

        self.SERIAL.timeout = 15
        # return self.query1(QUERY_STRING=QUERY_STRING,
        #                    SLEEP=15,
        #                    SHOW_ERROR=SHOW_ERROR,
        #                    SER_READ=SER_READ,
        #                    ERROR_HANDLER1=ERROR_HANDLER1,
        #                    SIGNAL_DELAY=SIGNAL_DELAY,
        #                    USE_READLINE=USE_READLINE,
        #                    ALLOW_UNSTABLE=ALLOW_UNSTABLE)

        query_success = False
        try:

            query_success = self.query2(query_string=QUERY_STRING,
                                        show_error=SHOW_ERROR,
                                        allow_unstable=ALLOW_UNSTABLE)

        except OSError as e:
            print "Some serious problem is going on..."

        except Exception as e:
            print "No idea whats wrong"

        finally:
            return query_success

    def query2(self, query_string="2008:3", show_error=False, allow_unstable=False):

        _ERROR_BOOL = False

        try:
            #serielle schnittstelle bereinigen
            self.SERIAL.flush()
            self.SERIAL.flushInput()
            self.SERIAL.flushOutput()

            self.write_line("%R1Q," + query_string + self.line_end)
            time.sleep(.1)
            t_out = self.read_line()
            t_out = t_out.replace("\r", "")

            # print "t_out: ", t_out.replace("\n", "").replace("\r", "")
            # print ""

            "Suche nach korrekten GeoCOM Output"

            m = re.search(r"((?P<geoCOMReplyType>\%R1P,)(?P<geoCOMReturnCode>\d))?((,)(?P<transactionID>\d))(:)(?P<returnCode>\d+)?(?P<parameter>.*)(\n)", t_out)

            "Lese GeoCOM Output"

            if m is not None:
                # print "m: ", m.groupdict()
                self.OUT = t_out.replace("\n", "")
                self.RETURNCODE = m.group("returnCode")
                self.ERRORCODE = ""
                self.PARAMETER = m.group("parameter")[1:]
                #_ERROR_BOOL = False
            else:
                self.RETURNCODE = "-1"
                self.ERRORCODE = "Incorrect TPS output for query %s" % query_string
                #_ERROR_BOOL = False

            "Bewertung von GeoCOM Output"

            if self.RETURNCODE == "0":
                _ERROR_BOOL = True

            elif allow_unstable and self.RETURNCODE == "1284":
                _ERROR_BOOL = True

            elif int(self.RETURNCODE) in GEOCOM_RETURNCODES.ReturnCodeDict:
                _ERROR_BOOL = False
                if show_error:
                    GeoCOMError("GeoCOM::Q %-10s... " % query_string[:10], "::R %-6s: %s" % (str(self.RETURNCODE)[:6], GEOCOM_RETURNCODES.ReturnCodeDict[int(self.RETURNCODE)]))
            else:
                _ERROR_BOOL = False
                if show_error:
                    GeoCOMError("GeoCOM::Q %-5s... " % query_string[:5], "::%-13s" % "UNBEKANNT")

        except Exception as e:
            print e
            _ERROR_BOOL = False

        finally:
            return _ERROR_BOOL

    def query1(self,
               QUERY_STRING='2008:%d' % TMC.TMC_CLEAR,
               SLEEP=0.0,
               SHOW_ERROR=True,
               SER_READ=10,
               ERROR_HANDLER1=True,
               SIGNAL_DELAY=None,
               USE_READLINE=True,
               ALLOW_UNSTABLE=False):

        _tic1 = time.time()
        _ERROR_BOOL = False
        signal_delay = self.SIGNAL_DELAY if not SIGNAL_DELAY else SIGNAL_DELAY

        if signal_delay > self.TIMEOUT:
            self.TIMEOUT = signal_delay

        loop_wait = SLEEP if SLEEP > signal_delay else signal_delay
        #LOOP_WAIT = 30
        try_count = 1
        while ((time.time() - _tic1) < loop_wait) and not _ERROR_BOOL:
            # print "Try #: %d" % try_count
            try:
                _ERROR_BOOL = self.single_query(QUERY_STRING=QUERY_STRING,
                                                SLEEP=SLEEP,
                                                SHOW_ERROR=SHOW_ERROR,
                                                SER_READ=SER_READ,
                                                ERROR_HANDLER1=ERROR_HANDLER1,
                                                SIGNAL_DELAY=SIGNAL_DELAY,
                                                USE_READLINE=USE_READLINE,
                                                ALLOW_UNSTABLE=ALLOW_UNSTABLE)

                wait_time = 0.1

                if not _ERROR_BOOL:
                    raise Exception("GeoCOM False argument")

            except IndexError:
                print "IndexError...cleaning Cache"
                wait_time = 3

            except Exception as e:
                print e
                wait_time = 3

            finally:
                # print "wait_time set to %f" % wait_time
                try_count += 1
                self.SERIAL.flush(); self.SERIAL.flushInput(); self.SERIAL.flushOutput()
                time.sleep(wait_time)

        if not _ERROR_BOOL:
            if self.RETURNCODE == "-999":
                raise ERROR.ConnectionError("TACHY-TPS", self.NAME)
            else:
                raise ERROR.SensorRequestError(self.NAME, self.RETURNCODE)

        return _ERROR_BOOL

    def testConnection(self, retries=1):
        """
        Überprüft, ob Verbindung mit dem Gerät besteht
        :rtype: `bool <https://docs.python.org/2/library/functions.html#bool>`_
        :return:    True, wenn das Gerät erreichbar war, sonst False
        """

        test_result = False
        while retries > 0:
            try:
                test_result = self.COM_NullProc()

            except:
                test_result = False

            finally:
                retries -= 1

        return test_result

    def load_serial_number(self):
        _RES = self.CSV_GetInstrumentNo()
        self.SERIAL_NUMBER = _RES['INSTRUMENT_NUMBER']
        return self.SERIAL_NUMBER

    def load_name(self):
        _RES = self.CSV_GetInstrumentName()
        self.NAME = _RES['INSTRUMENT_NAME']
        return self.NAME

    def is_horizonted(self):
        """
        Checks if the Device is horizonted properly by sending a "get angle"-Command
        and reading from it's Return Code.
        :return: True if horizonted, False if not, None if any other error occurs.
        """
        TRY_QUERY = self.query('2001:', SER_READ=1, SHOW_ERROR=False)
        if self.RETURNCODE == '0': return True
        if self.RETURNCODE == '1283': return False
        return None

    def COM_NullProc(self):
        """
        ASCII-Request: %R1Q,0:\n
        ASCII-Response: %R1P,0,0:RC\n
        Remarks: \n
        This function does not provide any functionality except of checking if the communication is up and running.
        """
        try:
            TRY = self.single_query('0:', SHOW_ERROR=False)
        except IndexError:
            TRY = False
        return TRY

    def COM_SwitchOnTPS(self):
        """
        ASCII-Request: %R1Q,111:eOnMode[short]\n
        ASCII-Response: \n
        If instrument is already switched on then %R1P,0,0:5
        else Nothing
        Remarks:\n
        This function switches on the TPS1200 instrument.
        Note: The TPS1200 instrument can be switched on by any

        :rtype: `bool <https://docs.python.org/2/library/functions.html#bool>`_
        :return: If query succeeded or not
        """

        TRY = self.single_query('111:1', SHOW_ERROR=False)
        return TRY

    def COM_SwitchOffTPS(self, eOffMode=MAIN.OFF):
        """
        ASCII-Request: %R1Q,112:eOffMode[short]\n
        ASCII-Response: %R1P,0,0:RC\n
        Remarks: This function switches off the TPS1200 instrument.

        :rtype: `bool <https://docs.python.org/2/library/functions.html#bool>`_
        :return: If query succeeded or not
        """
        TRY = self.single_query("112:%d" % (eOffMode))
        return TRY

    def EDM_Laserpointer_ON(self):
        """
        Schaltet den Laserpointer des Tachymeters EIN.
        """
        self.query('1004:%d' % MAIN.ON, SER_READ=1)
        if self.RETURNCODE == '0':
            return True
        else:
            self.ERRORCODE += self.RETURNCODE + ":: "
            return False

    def EDM_Laserpointer_OFF(self):
        """
        Schaltet den Laserpointer des Tachymeters AUS.
        """
        self.query('1004:%d' % MAIN.OFF, SER_READ=1)
        if self.RETURNCODE == '0':
            return True
        else:
            self.ERRORCODE += self.RETURNCODE + ":: "
            return False

    def TMC_GetAngle1(self, INC_Mode=TMC.TMC_MEA_INC, UNIT='gon', SER_READ=1):
        """
        ASCII-Request: %R1Q,2003:Mode[long]\n
        ASCII-Response: %R1P,0,0:RC,Hz[double],V[double],AngleAccuracy[double],
        AngleTime[long],CrossIncline[double],LengthIncline[double], AccuracyIncline[double],InclineTime[long],FaceDef[long]
        Remarks:\n
        This function carries out an angle measurement and, in dependence of configuration, inclination measurement
        and returns the results. As shown the result is very comprehensive. For simple angle measurements use
        TMC_GetAngle5 or TMC_GetSimpleMea instead.
        Information about measurement is returned in the return code.

        :type   INC_Mode            : int
        :param  INC_Mode            : Inclination Mode (default = 0)
        :type   UNIT                : str
        :param  UNIT                : converts measurement from [rad] to [UNIT] (default='gon')
        :type   SER_READ            : int
        :param  SER_READ            : define dump size if query uses Serial.read(SER_READ) instead of Serial.readline()

        :rtype: dict
        :return: HORIZONTAL_ANGLE, VERTICAL_ANGLE, ANGLE_ACCURACY, ANGLE_TIME, CROSS_INCLINE, LENGTH_INCLINE, ACCURACY_INCLINE, INCLINE_TIME, FACE_DEF
        """

        if UNIT == 'rad':
            CIRCLE = math.pi
        elif UNIT == 'gon':
            CIRCLE = 200
        else:
            return {}
        TRY_QUERY = self.query('2003:', SER_READ=SER_READ)
        # print self.ERRORCODE
        # if self.RETURNCODE == '0':
        if TRY_QUERY:
            ANGLE1 = self.PARAMETER.split(",")
            return {'HORIZONTAL_ANGLE': float(ANGLE1[0]) * CIRCLE / math.pi,
                    'VERTICAL_ANGLE': float(ANGLE1[1]) * CIRCLE / math.pi,
                    'ANGLE_ACCURACY': float(ANGLE1[2]) * CIRCLE / math.pi,
                    'ANGLE_TIME': float(ANGLE1[3]),
                    'CROSS_INCLINE': float(ANGLE1[4]) * CIRCLE / math.pi,
                    'LENGTH_INCLINE': float(ANGLE1[5]) * CIRCLE / math.pi,
                    'ACCURACY_INCLINE': float(ANGLE1[6]) * CIRCLE / math.pi,
                    'INCLINE_TIME': float(ANGLE1[7]),
                    'FACE': int(ANGLE1[8])}
        else:
            self.ERRORCODE += "2003:,RC: %s" % self.RETURNCODE
            # print self.OUT
            return {}

    def TMC_DoMeasure(self,
                      TMC_Mode=TMC.TMC_DEF_DIST,
                      EDM_Mode=EDM.EDM_SINGLE_TAPE):
        """
        ASCII-Request: %R1Q,2008:Command[long],Mode[long]\n
        ASCII-Response: %R1P,0,0:RC\n
        Remarks:\n
        This function carries out a distance measurement according to the TMC measurement mode like single distance,
        tracking,... . Please note that this command does not output any values (distances). In order to get the values
        you have to use other measurement functions such as TMC_GetCoordinate, TMC_GetSimpleMea or TMC_GetAngle.
        The result of the distance measurement is kept in the instrument and is valid to the next TMC_DoMeasure
        command where a new distance is requested or the distance is clear by the measurement program TMC_CLEAR.

        :param TMC_Mode:
        :param EDM_Mode:
        :return:
        """

        self.query('2008:%d,%d' % (TMC_Mode, EDM_Mode), SER_READ=1)

        if self.RETURNCODE == '0':
            return True
        else:
            self.ERRORCODE += ('2008:%d,%d' % (TMC_Mode, EDM_Mode)) + ' - ' + self.RETURNCODE + ":: "
            return False

    def TMC_GetStation(self):
        """
        ASCII-Request: %R1Q,2009:\n
        ASCII-Response: %R1P,0,0:RC,E0[double],N0[double],H0[double],Hi[double]\n
        Remarks:\n
        This function is used to get the station coordinates of the instrument.
        """
        TRY_QUERY = self.query('2009:', SER_READ=1)
        if TRY_QUERY:
            STATION = self.PARAMETER.split(",")
            return {'EASTING': float(STATION[0]),
                    'NORTHING': float(STATION[1]),
                    'HEIGHT': float(STATION[2]),
                    'INSTRUMENT_HEIGHT': float(STATION[3])}
        else:
            self.ERRORCODE += '2009:' + ' - ' + self.RETURNCODE + ":: "
            # print self.OUT
            return {}

    def TMC_SetStation(self, E0=0.0, N0=0.0, H0=0.0, Hi=0.0):
        """
        ASCII-Request: %R1Q,2010:E0[double],N0[double],H0[double],Hi[double]\n
        ASCII-Response: %R1P,0,0:RC\n
        Remarks:\n
        This function is used to set the station coordinates of the instrument.
        """
        self.query("2010:%f,%f,%f,%f" % (E0, N0, H0, Hi), SER_READ=1)
        if self.RETURNCODE == '0':
            return True
        else:
            self.ERRORCODE += "2010:%f,%f,%f,%f" % (E0, N0, H0, Hi) + ' - ' + self.RETURNCODE + ":: "
            return False

    def TMC_GetHeight(self):
        """
        ASCII-Request: %R1Q,2011:\n
        ASCII-Response: %R1P,0,0:RC,Height[double]\n
        Remarks:\n
        This function returns the current reflector height.
        :rtype: dict
        :return: REFLECTOR_HEIGHT
        """
        TRY = self.query("2011:")
        if TRY:
            HEIGHT = self.PARAMETER.split(",")
            return {'REFLECTOR_HEIGHT': float(HEIGHT[0])}
        if self.RETURNCODE == '0':
            return True
        else:
            self.ERRORCODE += '2011: - ' + self.RETURNCODE + ":: "
            return {}

    def TMC_SetHeight(self, REFLECTOR_HEIGHT=0.0):
        """
        ASCII-Request: %R1Q,2012:Height[double]\n
        ASCII-Response: %R1P,0,0:RC\n
        Remarks:\n
        This function sets a new reflector height.
        """
        if REFLECTOR_HEIGHT is not None:
            self.query("2012:%f" % REFLECTOR_HEIGHT)
            if self.RETURNCODE == '0':
                return True
            else:
                self.ERRORCODE += "2012:%f" % REFLECTOR_HEIGHT + ' - ' + self.RETURNCODE + ":: "
                return False
        else:
            return False

    def TMC_SetEdmMode(self,
                       EDM_Mode=EDM.EDM_SINGLE_STANDARD):
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

        :type   EDM_Mode            : int
        :param  EDM_Mode            : EDM Mode (default = 2)

        """

        self.query('2020:%d' % (EDM_Mode), SER_READ=1)
        if self.RETURNCODE == '0':
            return True
        else:
            self.ERRORCODE += '2020:%d' % EDM_Mode + ' - ' + self.RETURNCODE + ":: "
            return False

    def TMC_GetPrismCorr(self):
        """
        ASCII-Request: %R1Q,2023:\n
        ASCII-Response: %R1P,0,0:RC,PrismCorr[double]\n
        Remarks:\n
        This function is used to get the prism constant.
        :return:
        """
        self.query('2023:', SER_READ=1)
        if self.RETURNCODE == '0':
            prism_corr = self.PARAMETER.split(",")
            return {'PRISM_CORR': float(prism_corr[1])}
        else:
            self.ERRORCODE += '2023:' + ' - ' + self.RETURNCODE + ":: "
            return {}

    def TMC_GetFace(self):
        """
        ASCII-Request: %R1Q,2026:\n
        ASCII-Response: %R1P,0,0:RC,Face[long]\n
        Remarks:\n
        This function returns the face information of the current telescope position. The face information is only valid, if
        the instrument is in an active measurement state (that means a measurement function was called before the
        TMC_GetFace call, see example). Note that the instrument automatically turns into an inactive measurement
        state after a predefined timeout.

        :rtype: dict (FACE)
        :return: Lage des Tachymeters
        """
        time.sleep(1)
        TRY = self.single_query()
        if TRY:
            TRY = self.query('2026:')
            if TRY:
                # print self.OUT
                if self.RETURNCODE == '0':
                    return {'FACE': int(self.PARAMETER.split(",")[0])}
                else:
                    self.ERRORCODE += '2026:' + ' - ' + self.RETURNCODE + ":: "
                    return {}
            else:
                return {}
        else:
            return {}

    def TMC_SetAtmCorr(self, Lambda, Pressure, DryTemperature, WetTemperature):
        """
        ASCII-Request: %R1Q,2028:Lambda[double],Pressure[double], DryTemperature[double],WetTemperature[double]\n
        ASCII-Response: %R1P,0,0:RC,\n
        Remarks:\n
        This function is used to set the parameters for the atmospheric correction.

        :type   Lambda              : float
        :param  Lambda              : Lambda Zahl
        :type   Pressure            : float
        :param  Pressure            : Luftdruck
        :type   DryTemperature      : float
        :param  DryTemperature      : Virtuelle (trockene) Temperatur
        :type   WetTemperature      : float
        :param  WetTemperature      : Feuchte Temperatur

        :rtype: `bool <https://docs.python.org/2/library/functions.html#bool>`_
        :return: liefert True, wenn atmosphärische Korrektur gesetzt werden konnte, sonst False
        """
        self.query('2028:%f,%f,%f,%f' % (Lambda, Pressure, DryTemperature, WetTemperature), SER_READ=1)
        if self.RETURNCODE == '0':
            return True
        else:
            self.ERRORCODE += self.RETURNCODE + ":: "
            return False

    def TMC_GetAngle5(self,
                      INC_Mode=TMC.TMC_AUTO_INC,
                      UNIT='gon',
                      SER_READ=1):
        """
        ASCII-Request: %R1Q,2107:Mode[long]\n
        ASCII-Response: %R1P,0,0:RC,Hz[double],V[double]\n
        Remarks:\n
        This function carries out an angle measurement and returns the results. In contrast to the function
        TMC_GetAngle1 this function returns only the values of the angle. For simple angle measurements use
        TMC_GetSimpleMea instead.
        Information about measurement is returned in the return code.

        :type   INC_Mode            : int
        :param  INC_Mode            : Inclination Mode (default = 0)
        :type   UNIT                : str
        :param  UNIT                : converts measurement from [rad] to [UNIT] (default='gon')
        :type   SER_READ            : int
        :param  SER_READ            : define dump size if query uses Serial.read(SER_READ) instead of Serial.readline()

        :rtype: dict
        :return: HORIZONTAL_ANGLE, VERTICAL_ANGLE
        """

        if UNIT == 'rad':
            CIRCLE = math.pi
        elif UNIT == 'gon':
            CIRCLE = 200
        else:
            return {}
        self.query('2107:%d' % INC_Mode, SER_READ=SER_READ)
        if self.RETURNCODE == '0':
            try:
                ANGLE5 = self.PARAMETER.split(",")
                return {'HORIZONTAL_ANGLE': float(ANGLE5[0]) * CIRCLE / math.pi,
                        'VERTICAL_ANGLE': float(ANGLE5[1]) * CIRCLE / math.pi}
            except:
                return {}
        else:
            self.ERRORCODE += self.RETURNCODE + ":: "
            return {}

    def TMC_GetSimpleMea(self, WaitTime=MAIN.WAIT_TIME, INC_Mode=TMC.TMC_AUTO_INC, UNIT='gon', ALLOW_UNSTABLE=False):
        """
        ASCII-Request: %R1Q,2108:WaitTime[long],Mode[long]\n
        ASCII-Response: %R1P,0,0:RC,Hz[double],V[double],SlopeDistance[double]\n
        Remarks:\n
        This function returns the angles and distance measurement data. This command does not issue a new distance
        measurement. A distance measurement has to be started in advance. If a distance measurement is valid the
        function ignores WaitTime and returns the results. If no valid distance measurement is available and the
        distance measurement unit is not activated (by TMC_DoMeasure before the TMC_GetSimpleMea call) the angle
        measurement result is returned after the waittime. Information about distance measurement is returned in the
        return code.

        :type   INC_Mode            : int
        :param  INC_Mode            : Inclination Mode (default = 0)
        :type   UNIT                : str
        :param  UNIT                : converts measurement from [rad] to [UNIT] (default='gon')
        :type   WaitTime            : int
        :param  WaitTime            : Waiting [ms] to collect TACHY data

        :rtype: dict
        :return: HORIZONTAL_ANGLE, VERTICAL_ANGLE, ANGLE_ACCURACY, ANGLE_TIME, CROSS_INCLINE, LENGTH_INCLINE, ACCURACY_INCLINE, INCLINE_TIME, FACE_DEF
        """

        if UNIT == 'rad':
            CIRCLE = math.pi
        elif UNIT == 'gon':
            CIRCLE = 200
        else:
            return {}

        self.query('2108:%d,%d' % (WaitTime, INC_Mode), SER_READ=1)
        if self.RETURNCODE == '0' or (self.RETURNCODE == '1284' and ALLOW_UNSTABLE):
            SIMPLE_MEA = self.PARAMETER.split(",")

            return {'HORIZONTAL_ANGLE': float(SIMPLE_MEA[0]) * CIRCLE / math.pi,
                    'VERTICAL_ANGLE': float(SIMPLE_MEA[1]) * CIRCLE / math.pi,
                    'SLOPE_DISTANCE': float(SIMPLE_MEA[2])}
        else:
            self.ERRORCODE += '2108:%d,%d' % (WaitTime, INC_Mode) + ' - ' + self.RETURNCODE + ":: "
            return {}

    def TMC_SetOrientation(self, HzOrientation=0):
        """
        ASCII-Request: %R1Q,2113:HzOrientation[double]\n
        ASCII-Response: %R1P,0,0:RC\n
        Remarks:\n
        This function is used to orientate the instrument in Hz direction. It is a combination of an angle measurement to
        get the Hz offset and afterwards setting the angle Hz offset in order to orientates onto a target. Before the new
        orientation can be set an existing distance must be cleared (use TMC_DoMeasure with the command =
        TMC_CLEAR).
        """
        self.TMC_DoMeasure(TMC_Mode=TMC.TMC_CLEAR)
        self.TMC_GetAngle1()
        TRY = self.query("2113:%f" % ANGLE.gon2rad(HzOrientation), SLEEP=0.001, SER_READ=1)
        return TRY

    def TMC_GetSimpleCoord(self, WaitTime=MAIN.WAIT_TIME, INC_Mode=TMC.TMC_AUTO_INC, ALLOW_UNSTABLE=False):
        """
        ASCII-Request: %R1Q,2116:WaitTime[long],eProg[long]\n
        ASCII-Response: %R1P,0,0:RC,dCoordE[double], dCoordN[double], dCoordH[double]\n
        Remarks:\n
        This function gets the cartesian co-ordinates if a valid distance exists. The parameter WaitTime defined the
        max wait time in order to get a valid distance. If after the wait time a valid distance does not exist, the function
        initialises the parameter for the co-ordinates (E,N,H) with 0 and returns an error. For the co-ordinate calculate
        will require incline results. With the parameter eProg you have the possibility to either measure an inclination,
        use the pre-determined plane to calculate an inclination, or use the automatic mode wherein the system decides
        which method is appropriate (see 15.1.1).
        """
        self.query('2116:%d,%d' % (WaitTime, INC_Mode), SLEEP=2, SER_READ=1)
        if (self.RETURNCODE == '0' or (self.RETURNCODE == '1284' and ALLOW_UNSTABLE)):
            COORDS = self.PARAMETER.split(",")
            return {'EASTING': float(COORDS[0]),
                    'NORTHING': float(COORDS[1]),
                    'HEIGHT': float(COORDS[2])}
        else:
            return {}

    def TMC_QuickDist(self, UNIT='gon', ALLOW_UNSTABLE=False):
        """
        ASCII- Request: %R1Q,2117:\n
        ASCII-Response: %R1P,0,0:RC,dHz[double],dV[double],dSlopeDistance[double]\n
        Remarks:\n
        The function starts an EDM Tracking measurement and waits until a distance is measured. Then it returns the
        angle and the slope-distance, but no co-ordinates. If no distance can be measured, it returns the angle values (hz,
        v) and the corresponding return-code.
        In order to abort the current measuring program use the function TMC_DoMeasure.

        :rtype: dict
        :return: HORIZONTAL_ANGLE, VERTICAL_ANGLE, SLOPE_DISTANCE
        """
        if UNIT == 'gon': CIRCLE = 200
        elif UNIT == 'rad': CIRCLE = math.pi
        else: CIRCLE = 200

        self.query("2117:", SER_READ=1)
        if self.RETURNCODE == '0' or (self.RETURNCODE == '1284' and ALLOW_UNSTABLE):
            QUICK_DIST = self.PARAMETER.split(",")
            return {'HORIZONTAL_ANGLE': float(QUICK_DIST[0]) * CIRCLE / math.pi,
                    'VERTICAL_ANGLE': float(QUICK_DIST[1]) * CIRCLE / math.pi,
                    'SLOPE_DISTANCE': float(QUICK_DIST[2])}

    def TMC_GetSlopeDistCorr(self):
        """
        ASCII-Request: %R1Q,2126:\n
        ASCII-Response: %R1P,0,0: RC,dPpmCorr[double], dPrismCorr[double]\n
        Remarks:\n
        This function retrieves the total ppm value (atmospheric+geometric ppm) plus the current prism constant.
        """
        self.query('2126:', SER_READ=1)
        if self.RETURNCODE == '0':
            SLOPE_DIST_CORR = self.PARAMETER.split(",")
            return {'PPM_CORR': float(SLOPE_DIST_CORR[0]),
                    'PRISM_CORR': float(SLOPE_DIST_CORR[1])}
        else:
            self.ERRORCODE += '2126:' + ' - ' + self.RETURNCODE + ":: "
            return {}

    def CSV_GetInstrumentNo(self):
        """
        ASCII-Request: %R1Q,5003:\n
        ASCII-Response: %R1P,0,0:RC, SerialNo[long]\n
        Remarks:\n
        Gets the factory defined serial number of the instrument.
        """
        self.query('5003:', SER_READ=1)
        if self.RETURNCODE == '0':
            SNR = self.PARAMETER.split(",")[0]
            return {'INSTRUMENT_NUMBER': SNR}
        else:
            self.ERRORCODE += self.RETURNCODE + ":: "
            return {}

    def CSV_GetInstrumentName(self):
        """
        ASCII-Request: %R1Q,5004:\n
        ASCII-Response: %R1P,0,0:RC,Name[string]\n
        Remarks:\n
        Gets the instrument name, for example: TCRP1201 R300

        :rtype: dict
        :return: INSTRUMENT_NAME
        """
        self.query('5004:', SER_READ=1)
        if self.RETURNCODE == '0':
            NAME = self.PARAMETER.split(",")[0]
            return {'INSTRUMENT_NAME': NAME}
        else:
            self.ERRORCODE += self.RETURNCODE + ":: "
            return {}

    def CSV_GetIntTemp(self):
        """
        ASCII-Request: %R1Q,5011:\n
        ASCII-Response: %R1P,0,0:RC,Temp[long]\n
        Remarks:\n
        Get the internal temperature of the instrument, measured on the Mainboard side. Values are reported in degrees
        Celsius.

        :rtype: dict
        :return: TEMPERATURE
        """
        self.query('5011:', SER_READ=1)
        if self.RETURNCODE == '0':
            TEMP = float(self.PARAMETER.split(",")[0])
            return {'TEMPERATURE': TEMP}
        else:
            self.ERRORCODE += '5011:' + ' - ' + self.RETURNCODE + ":: "
            return {}

    def AUT_SetTol(self, ToleranceHz=MAIN.DHZ, ToleranceV=MAIN.DV):
        """
        ASCII-Request: %R1Q,9007:ToleranceHz[double], Tolerance V[double]\n
        ASCII-Response: %R1P,0,0:RC\n
        Remarks:\n
        This command sets new values for the positioning tolerances of the Hz- and V- instrument axes. This command
        is valid for motorized instruments only.
        The tolerances must be in the range of 1[cc] ( =1.57079 E-06[rad] ) to 100[cc] ( =1.57079 E-04[rad] )

        """
        self.query(QUERY_STRING='9007:%f,%f' % (ToleranceHz, ToleranceV), SLEEP=0, SHOW_ERROR=False, SER_READ=1, ERROR_HANDLER1=False)
        if self.RETURNCODE == '0':
            return True
        else:
            return False

    def AUT_SetTimeOut(self, time_out_hz=20, time_out_v=20):
        """
        ASCII-Request: %R1Q,9011:TimeoutHz[double],TimeoutV[double] \n
        ASCII-Response: %R1P,0,0:RC \n
        Remarks:\n
        This command set the positioning timeout (set maximum time to perform a positioning). The timeout is reset on
        10[sec] after each power on
        """
        self.query(QUERY_STRING='9011:%f,%f' % (time_out_hz, time_out_v),
                   SLEEP=0,
                   SHOW_ERROR=False,
                   SER_READ=1,
                   ERROR_HANDLER1=False)

        if self.RETURNCODE == '0':
            return True
        else:
            return False

    def AUT_LockIn(self):
        """
        ASCII-Request: %R1Q,9013:\n
        ASCII-Response: %R1P,0,0:RC\n
        Remarks:\n
        If LOCK mode is activated (AUS_SetUserLockState) then the function starts the target tracking. The
        AUT_LockIn command is only possible if a AUT_FineAdjust command has been previously sent and
        successfully executed.
        """
        self.query("9013:")
        if self.RETURNCODE == '0': return True
        else: return False

    def AUT_MakePositioning(self, Hz=0.0, V=100.0, PosMode=AUT.AUT_NORMAL, ATRMode=AUT.AUT_POSITION):
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

        :type   Hz                  : float
        :param  Hz                  : Positioning Angle Hz [gon]
        :type   V                   : float
        :param  V                   : Positioning Angle V [gon]
        :type   PosMode             : int
        :param  PosMode             : Positioning mode (default = 0)
        :type   ATRMode             : int
        :param  ATRMode             : ATR Mode (default = 0)
        """
        self.query('9027:%f,%f,%d,%d,0' % (ANGLE.gon2rad(Hz), ANGLE.gon2rad(V), PosMode, ATRMode),
                   SLEEP=5.9,
                   SER_READ=100,
                   SIGNAL_DELAY=8)
        if self.RETURNCODE == '0':
            return True
        else:
            self.ERRORCODE += '9027:%f,%f,%d,%d,0' % (Hz, V, PosMode, ATRMode) + ' - ' + self.RETURNCODE + ":: "
            return False

    def AUT_ChangeFace(self, SER_READ=1000, SLEEP=6.5):
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

        :type   SER_READ            : int
        :param  SER_READ            : characters to read if query is set to use Serial.read(SER_READ) insteat of Serial.readline()
        :type   SLEEP               : float
        :param  SLEEP               : Giving the TACHY some time to change face.
        """
        self.query('9028:', SLEEP=SLEEP, SER_READ=SER_READ)
        if self.RETURNCODE == '0':
            return True
        else:
            self.ERRORCODE += self.RETURNCODE
            return False

    def AUT_FineAdjust(self, dSrchHz=MAIN.DHZ, dSrchV=MAIN.DV):
        """
        ASCII-Request: %R1Q,9037: dSrchHz[double], dSrchV[double],0\n
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

        :type   dSrchHz             : float
        :param  dSrchHz             : Search Window Hz [rad]
        :type   dSrchV              : float
        :param  dSrchV              : Search Window V [rad]
        """
        TRY = self.query('9037:%f,%f,0' % (dSrchHz, dSrchV), SER_READ=1)
        if TRY:
            if self.RETURNCODE == '0':
                return True
            else:
                self.ERRORCODE += '9037:%f,%f' % (dSrchHz, dSrchV) + ' - ' + self.RETURNCODE + ":: "
                return False
        else:
            return False

    def AUT_GetUserSpiral(self):
        """
        ASCII-Request: %R1Q,9040\n
        ASCII-Response: %R1P,0,0:RC,dRangeHz[double],dRangeV[double]\n
        Remarks:\n
        This function returns the current dimension of ATR search window. This command is valid for all instruments,
        but has only affects automated instruments.
        """
        self.query("9040:")
        UserSpiral = self.PARAMETER.split(",")
        if self.RETURNCODE == '0':
            return {'DRANGE_HZ': float(UserSpiral[0]),
                    'DRANGE_V': float(UserSpiral[1])}
        else:
            return {}

    def AUT_SetUserSpiral(self, DRANGE_HZ=1e-4, DRANGE_V=1e-4):
        """
        ASCII-Request: %R1Q,9041:dRangeHz,dRangeV[double]\n
        ASCII-Response: %R1P,0,0:RC\n
        Remarks:\n
        This function sets the dimension of the ATR search
        """
        self.query("9041:%f,%f" % (DRANGE_HZ, DRANGE_V))
        return True if self.RETURNCODE == '0' else False

    def BAP_SetPrismType(self, PrismType=BAP.BAP_PRISM_MINI):
        """
        ASCII-Request: %R1Q,17008: ePrismType [long]\n
        ASCII-Response: %R1P,0,0:RC\n
        Remarks:\n
        Sets the prism type for measurements with a reflector. It overwrites the prism constant, set by
        TMC_SetPrismCorr.

        :type   PrismType           : int
        :param  PrismType           : Prism Type (default = 1)
        """
        self.query('17008:%d' % PrismType, SER_READ=1)

        if self.RETURNCODE == '0':
            return True
        else:
            self.ERRORCODE += '17008:%d' % PrismType + ' - ' + self.RETURNCODE + ":: "
            return False

    def BAP_GetPrismType(self):
        """
        ASCII-Request: %R1Q,17009:\n
        ASCII-Response: %R1Q,0,0:RC, ePrismType[long]\n
        Remarks:\n
        Gets the current prism type.

        :rtype: dict
        :return: PRISM_TYPE
        """
        self.query('17009:', SER_READ=1)
        temp_result = self.PARAMETER.split(",")
        if self.RETURNCODE == '0':
            return {'PRISM_TYPE': int(temp_result[0])}
        else:
            self.ERRORCODE += self.RETURNCODE + ":: "
            return {}

    def AUS_SetUserAtrState(self, OnOff=AUT.AUT_TARGET):
        """
        ASCII-Request: %R1Q,18005:On/Off[long]\n
        ASCII-Response: %R1P,0,0:RC\n
        Remarks:\n
        Activates respectively deactivates the ATR mode.\n
        Activate ATR mode:\n
        The ATR mode gets activated. If LOCK mode is on and the command is sent, then LOCK mode changes to ATR
        mode.
        Deactivate ATR mode:\n
        The ATR mode gets deactivated. If LOCK mode is on and the command is sent, then LOCK mode stays on
        This command is valid for automated instrument models only.
        Refer to Table 6-1: Automation Modes for further information.

        :type   OnOff               : int
        :param  OnOff               : Un/Set ATR mode (default = 1)
        """
        self.query('18005:%d' % (OnOff), SER_READ=1)
        if self.RETURNCODE == '0': return True
        else:
            self.ERRORCODE += '18005:%d' % (OnOff) + ' - ' + self.RETURNCODE + ":: "
            return False

    def AUS_GetUserAtrState(self):
        """
        ASCII-Request: %R1Q,18006:\n
        ASCII-Response: %R1P,0,0:RC,OnOff[long]\n
        Remarks:\n
        Get the current status of the ATR mode on automated instrument models. This command does not indicate
        whether the ATR has currently acquired a prism. Note the difference between GetUserATR and GetUserLOCK
        state.
        """
        self.query('18006:', SER_READ=1)
        temp_result = self.PARAMETER.split(",")
        if self.RETURNCODE == '0':
            return {'ATR_MODE_STATE': int(temp_result[0])}
        else:
            self.ERRORCODE += self.RETURNCODE + ":: "
            return {}

    def AUS_SetUserLockState(self, OnOff=MAIN.OFF):
        """
        ASCII-Request: %R1Q,18007:OnOff[long]\n
        ASCII-Response: %R1P,0,0:RC\n
        Remarks:\n
        Activates or deactivates the LOCK mode.\n
        Status ON:\n
        The LOCK mode is activated. This does not mean that the instrument is locked onto a prism. In order to lock and
        follow a moving target, see the function AUT_LockIn.\n
        Status OFF:\n
        The LOCK mode is deactivated. A moving target, which is being tracked, will be aborted and the manual drive
        wheel is activated.\n
        This command is valid for automated instruments only.
        Refer to Table 6-1: Automation Modes for further information.

        :type   OnOff               : int
        :param  OnOff               : Un/Set LOCK mode (default = 0 = OFF)
        """
        self.query('18007:%d' % OnOff, SER_READ=1)
        if self.RETURNCODE == '0':
            return True
        else:
            self.ERRORCODE += '18007:%d' % OnOff + ' - ' + self.RETURNCODE + ":: "
            return False

    def AUS_GetUserLockState(self):
        """
        ASCII-Request: %R1Q,18008:\n
        ASCII-Response: %R1P,0,0:RC, OnOff[long]\n
        Remarks:\n
        This command gets the current status of the LOCK mode. This command is valid for automated instruments
        only. TheGetUserLockState command does not indicate if the instrument is currently locked to a prism. For this
        function the MotReadLockStatus has to be used.
        Refer to Table 6-1: Automation Modes for further information.

        :rtype: dict
        :return: LOCK_MODE_STATE
        """
        self.query('18008:', SER_READ=1)
        temp_result = self.PARAMETER.split(",")
        if self.RETURNCODE == '0':
            return {'LOCK_MODE_STATE': int(temp_result[0])}
        else:
            self.ERRORCODE += self.RETURNCODE + ":: "
            return {}

    def MOT_StopController(self, mode=MOT.MOT_NORMAL):
        """
        ASCII-Request: %R1Q,6002:mode[long]\n
        ASCII-Response: %R1P,0,0:RC\n
        Remarks:\n
        This command is used to stop movement and used to stop the motor controller operation.

        :type mode                  : int
        :param mode                 : Stop mode
        """
        self.query('6002:%d' % mode, SER_READ=1)
        if self.RETURNCODE == '0':
            return True
        else:
            self.ERRORCODE += '6002:%d' % mode + ' - ' + self.RETURNCODE + ":: "
            return False

    def MOT_StartController(self, ControlMode=MOT.MOT_OCONST):
        """
        ASCII-Request: %R1Q,6001:ControlMode[long]\n
        ASCII-Response: %R1P,0,0:RC\n
        Remarks:\n
        This command is used to enable remote or user interaction to the motor controller.

        :type ControlMode                  : int
        :param ControlMode                 : Controller mode. If used together with MOT_SetVelocity the control mode has to be MOT_OCONST.
        """
        self.query('6001:%d' % ControlMode, SER_READ=1)
        if self.RETURNCODE == '0':
            return True
        else:
            self.ERRORCODE += '6001:%d' % ControlMode + ' - ' + self.RETURNCODE + ":: "
            return False

    def MOT_SetVelocity(self, HZ_Speed=0.0, V_Speed=0.0):
        """
        ASCII-Request: %R1Q,6004:HZ-Speed[double],V-Speed[double]\n
        ASCII-Response: %R1P,0,0:RC\n
        Remarks:\n
        This command is used to set up the velocity of motorization.

        :type HZ_Speed                     : double
        :param HZ_Speed                    : Horizontal velocity setting in rad/s
        :type V_Speed                      : double
        :param V_Speed                     : Vertical velocity setting in rad/s
        """
        self.query('6004:%f,%f' % (HZ_Speed, V_Speed), SER_READ=1)
        if self.RETURNCODE == '0':
            return True
        else:
            self.ERRORCODE += '6004:%f,%f' % (HZ_Speed, V_Speed) + ' - ' + self.RETURNCODE + ":: "
            return False

    def BAP_MeasDistanceAngle(self, dist_mode=BAP.BAP_SINGLE_REF_VISIBLE, UNIT='gon'):
        """
        ASCII-Request: %R1Q,17017:DistMode[long]\n
        ASCII-Response: %R1P,0,0:RC,dHz[double],dV[double],dDist[double],DistMode[long]\n
        Remarks:\n
        This function measures angles and a single distance depending on the mode DistMode. Note that this function is
        not suited for continuous measurements (LOCK mode and TRK mode). This command uses the current automation
        settings.

        :param dist_mode:
        :return:
        """
        if UNIT == 'gon':
            CIRCLE = 200
        elif UNIT == 'rad':
            CIRCLE = math.pi
        else:
            CIRCLE = 200

        self.query("17017:%d" % dist_mode, SER_READ=1)
        if self.RETURNCODE == '0':
            value = self.PARAMETER.split(",")
            return {'HORIZONTAL_ANGLE': float(value[0]) * CIRCLE / math.pi,
                    'VERTICAL_ANGLE': float(value[1]) * CIRCLE / math.pi,
                    'SLOPE_DISTANCE': float(value[2]),
                    'DIST_MODE': int(value[3])}

    def BAP_SetMeasPrg(self, e_meas_prg=BAP.BAP_SINGLE_REF_STANDARD):
        """
        ASCII-Request: %R1Q,17019:eMeasPrg[long]\n
        ASCII-Response: %R1P,0,0:RC\n
        Remarks:\n
        Defines the distance measurement program i.e. for BAP_MeasDistanceAngle. RL EDM type programs are not available
        on all instrument types. Changing the measurement programs may change the EDM type as well (Reflector (IR)= and
        Reflectorless (RL)).

        :param e_meas_prg: Measurement Program
        :return:
        """
        self.query('17019:%d' % e_meas_prg, SER_READ=1)
        if self.RETURNCODE == '0':
            return True
        else:
            self.ERRORCODE += '17019:%d' % e_meas_prg + ' - ' + self.RETURNCODE + ":: "
            return False

    def LG_GetAll(self, UNIT='gon', SER_READ=1):
        if UNIT == 'rad':
            CIRCLE = math.pi
        elif UNIT == 'gon':
            CIRCLE = 200
        else:
            return {}

        self.query('2145:', SER_READ=SER_READ)
        if self.RETURNCODE == '0':
            temp_result = self.OUT.split(',')
            return {'SLOPE_DISTANCE': float(temp_result[15]),
                    'HORIZONTAL_ANGLE': float(temp_result[6]) * CIRCLE / math.pi,
                    'VERTICAL_ANGLE': float(temp_result[7]) * CIRCLE / math.pi,
                    'CROSS_INCLINE': float(temp_result[10]) * CIRCLE / math.pi,
                    'LENGTH_INCLINE': float(temp_result[11]) * CIRCLE / math.pi}
        else:
            self.ERRORCODE += '2145:' + ' - ' + self.RETURNCODE + ":: "
            return {}

    def get_HzV(self, ATR=True, UNIT='gon'):
        aim_at_target = True
        if ATR:
            aim_at_target = self.AUT_FineAdjust()

        self._OUT = self.TMC_GetAngle5(UNIT=UNIT) if aim_at_target else {}

        return self._OUT

    def set_tps(self,
                ATR_MODE=AUT.AUT_TARGET,
                EDM_MODE=EDM.EDM_SINGLE_STANDARD,
                TOL_HZ=MAIN.DHZ,
                TOL_V=MAIN.DV,
                position="TPS-Position"):

        ATR_MODE = AUT.AUT_TARGET if not ATR_MODE else ATR_MODE
        EDM_MODE = EDM.EDM_SINGLE_STANDARD if not EDM_MODE else EDM_MODE
        TOL_V = MAIN.DHZ if not TOL_V else TOL_V
        TOL_HZ = MAIN.DV if not TOL_HZ else TOL_HZ

        if not self.COM_NullProc():
            raise ERROR.ConnectionError(sensorType="TACHY",
                                        sensorPosition=position)

        self.TMC_DoMeasure(TMC.TMC_CLEAR)                     # Clean TPS data
        self.TMC_SetEdmMode(EDM_MODE)                         # Set EDM Mode
        self.AUS_SetUserAtrState(ATR_MODE)                    # Set ATR Mode
        self.AUT_SetTol(TOL_HZ, TOL_V)                        # Set ATR Tolerance in Hz and V direction
        self.TMC_DoMeasure(TMC.TMC_CLEAR)                     # Clean TPS data
        # self.SETATMOSPHERE                                    # Set Atmospheric Correction

    def turn_to2(self,
                 HORIZONTAL_ANGLE=None,
                 VERTICAL_ANGLE=None,
                 SEARCH_HORIZONTAL=1e-4,
                 SEARCH_VERTICAL=1e-4,
                 FACE=0,
                 FINE_ADJUST=True,
                 PosMode=AUT.AUT_PRECISE,
                 ATRMode=AUT.AUT_TARGET,
                 command_wait=5,
                 command_retry=3):

        setter_dict = []
        getter_dict = []

        # if self.TMC_GetFace()["FACE"] != int(FACE):
        #    setter_dict.append("self.AUT_ChangeFace()")
        # setter_dict.append("time.sleep(3)")

        if HORIZONTAL_ANGLE is not None and VERTICAL_ANGLE is not None:
            atr_mode = ATRMode if FINE_ADJUST else AUT.AUT_POSITION

            setter_dict.append("self.AUT_MakePositioning(%f,%f,%d,%d)" % (ANGLE.change_face_hz(HORIZONTAL_ANGLE, FACE),
                                                                          ANGLE.change_face_v(VERTICAL_ANGLE, FACE),
                                                                          PosMode,
                                                                          atr_mode))

            # setter_dict.append("time.sleep(3)")

        setter_dict.append("self.AUT_FineAdjust(%f,%f)" % (SEARCH_HORIZONTAL, SEARCH_VERTICAL))

        turn_out = self.do_dict(setter_dict=setter_dict,
                                getter_dict=getter_dict,
                                command_wait=command_wait,
                                command_retry=command_retry)

        if turn_out:
            return True

        else:
            return False

    def turn_to(self,
                HORIZONTAL_ANGLE=None,
                VERTICAL_ANGLE=None,
                SEARCH_HORIZONTAL=1e-4,
                SEARCH_VERTICAL=1e-4,
                FACE=0,
                FINE_ADJUST=True,
                PosMode=AUT.AUT_PRECISE,
                ATRMode=AUT.AUT_TARGET):
        """
        Dreht den TPS. Wenn FINE_ADJUST=False, dann wird der Zielpunkt nicht nachgeführt.

        :type HORIZONTAL_ANGLE: float
        :param HORIZONTAL_ANGLE: Turn instrument to Hz [gon]
        :type VERTICAL_ANGLE: float
        :param VERTICAL_ANGLE: Turn instrument to Hz [gon]
        :type SEARCH_HORIZONTAL: float
        :param SEARCH_HORIZONTAL: Search Window Hz [rad]
        :type SEARCH_VERTICAL: float
        :param SEARCH_VERTICAL: Search Window V [rad]
        :type FACE: int
        :param FACE: Face of TACHY (default = 0 [I])
        :type FINE_ADJUST: `bool <https://docs.python.org/2/library/functions.html#bool>`_
        :param FINE_ADJUST: Use AUT_FineAdjust (default = True)
        :type ATRMode: int
        :param ATRMode: ATR Modus laut GeoCom
        :type PosMode: int
        :param PosMode: PosMode laut GeoCom
        """

        TRY = True

        if TRY:
            TRY = self.TMC_GetFace()
            if not int(FACE) == int(TRY["FACE"]):
                self.AUT_ChangeFace()
            else:
                pass

        if HORIZONTAL_ANGLE and VERTICAL_ANGLE:
            # print "HZ,V: ",HORIZONTAL_ANGLE,VERTICAL_ANGLE,FACE
            ATRMode2 = ATRMode if FINE_ADJUST else AUT.AUT_POSITION
            self.COM_NullProc()
            TRY = self.AUT_MakePositioning(ANGLE.change_face_hz(HORIZONTAL_ANGLE, FACE),
                                           ANGLE.change_face_v(VERTICAL_ANGLE, FACE),
                                           PosMode,
                                           ATRMode2)

        if not TRY:
            raise ERROR.TargetError('TachyTarget', HORIZONTAL_ANGLE, VERTICAL_ANGLE)

        self.query()

        if TRY:
            if FINE_ADJUST:
                TRY = self.AUT_FineAdjust(SEARCH_HORIZONTAL, SEARCH_VERTICAL)     # Fine Adjust to prism

        return TRY

    def set_lock(self,
                 EDM_Mode=EDM.EDM_SINGLE_STANDARD,
                 TMC_Mode=TMC.TMC_STOP,
                 OnOff=MAIN.OFF):
        """

        :param EDM_Mode:
        :param TMC_Mode:
        :param OnOff:
        :return:
        """

        self.TMC_DoMeasure(TMC_Mode=TMC_Mode)
        if OnOff == 0:
            self.TMC_DoMeasure(TMC_Mode=TMC.TMC_CLEAR)
        self.AUS_SetUserAtrState(MAIN.ON)
        self.AUS_SetUserLockState(OnOff)
        self.TMC_SetEdmMode(EDM_Mode=EDM_Mode)
        if OnOff == 1:
            self.AUT_LockIn()

    def do_dict(self, setter_dict, getter_dict, command_retry=MAIN.COMMAND_RETRIES, command_wait=MAIN.COMMAND_WAIT):
        """

        :param setter_dict:
        :param getter_dict:
        :param command_retry:
        :param command_wait:
        :return:
        """
        setter_n = len(setter_dict)
        # setter_i = 0
        # setter_load = True
        # getter_n = len(getter_dict)
        # getter_i = 0
        # getter_load = True

        do_wait = command_wait
        measure_out = {}

        command_i = 0
        command_dict = setter_dict + getter_dict
        command_n = len(command_dict)
        command_load = True
        command_retries = 0

        while command_retries < command_retry and command_i < command_n:

            try:
#                print "DODICT: %s" % command_dict[command_i]
#                print "Command Retries: ", command_retries
                tmp_out = eval(command_dict[command_i])

                if tmp_out:
                    if command_i >= setter_n:
                        measure_out.update(tmp_out)
                    command_i += 1
                    do_wait = 0.1
                    command_load = True

                else:
                    command_load = False
                    command_i = 0
                    command_retries += 1
                #    raise Exception("Error in Command %s" % command_dict[command_i])

            except ERROR.ConnectionError as e:
                print e
                measure_out = {}
                command_load = False
                command_i = 0
                command_retries += 1
                do_wait = command_wait

            except ERROR.SensorRequestError as e:
                print e
                command_load = False
                command_i = 0
                command_retries += 1
                command_wait = MAIN.COMMAND_WAIT

            except TypeError as e:
                print e
                command_load = False
                command_i = 0
                command_retries += 1
                command_wait = MAIN.COMMAND_WAIT

            except Exception as e:
                print e
                command_load = False
                command_i = 0
                command_retries += 1
                command_wait = MAIN.COMMAND_WAIT

            except:
                command_load = False
                command_i = 0
                command_retries += 1
                command_wait = MAIN.COMMAND_WAIT

            finally:
                time.sleep(do_wait)

        if command_load:
            measure_out.update({'UID': GENERATES.gen_uuid(),
                                'SYNCED': 0,
                                'CREATED': GENERATES.gen_now(DATE_RETURN=True)})
        return measure_out

    def measure2(self,
                 HORIZONTAL_ANGLE=None,
                 VERTICAL_ANGLE=None,
                 REFLECTOR_HEIGHT=0.00,
                 SEARCH_HORIZONTAL=1e-4,
                 SEARCH_VERTICAL=1e-4,
                 PRISM_TYPE=BAP.BAP_PRISM_MINI,
                 # POS_MODE=AUT.AUT_NORMAL,
                 TMC_MODE=TMC.TMC_DEF_DIST,
                 INC_MODE=TMC.TMC_AUTO_INC,
                 FACE=0,
                 FINE_ADJUST=False,
                 WAIT_MEASURE=MAIN.WAIT_TIME,
                 # position="TACHY-TPS-Position",
                 # targetName='TachyTarget',
                 command_retry=MAIN.COMMAND_RETRIES,
                 command_wait=MAIN.COMMAND_WAIT):
        """

        :param HORIZONTAL_ANGLE:
        :param VERTICAL_ANGLE:
        :param REFLECTOR_HEIGHT:
        :param SEARCH_HORIZONTAL:
        :param SEARCH_VERTICAL:
        :param PRISM_TYPE:
        :param POS_MODE:
        :param TMC_MODE:
        :param INC_MODE:
        :param FACE:
        :param FINE_ADJUST:
        :param WAIT_MEASURE:
        :param position:
        :param targetName:
        :param command_retry:
        :param command_wait:
        :return: UID, SYNCED, CREATED, TEMPERATURE, PPM_CORR, PRISM_CORR, HORIZONTAL_ANGLE, VERTICAL_ANGLE, SLOPE_DISTANCE, CROSS_INCLINE, LENGTH_INCLINE, EASTING, NORTHING, HEIGHT, REFLECTOR_HEIGHT
        :rtype: dict
        """

        setter_dict = ["self.TMC_DoMeasure(3, 1)",
                       #"self.EDM_Laserpointer_ON()",
                       "self.BAP_SetPrismType(%d)" % PRISM_TYPE,
                       "self.TMC_SetHeight(%f)" % REFLECTOR_HEIGHT,
                       "self.turn_to2(HORIZONTAL_ANGLE=%s, VERTICAL_ANGLE=%s, SEARCH_HORIZONTAL=%s, SEARCH_VERTICAL=%s, FACE=%s, FINE_ADJUST=%s, command_retry=1, command_wait=0.1)" % (HORIZONTAL_ANGLE,
                                                                                                        VERTICAL_ANGLE,
                                                                                                        SEARCH_HORIZONTAL,
                                                                                                        SEARCH_VERTICAL,
                                                                                                        FACE,
                                                                                                        FINE_ADJUST),
                       "self.TMC_DoMeasure(%s, %s)" % (TMC_MODE, INC_MODE)]

        getter_dict = ["self.CSV_GetIntTemp()",
                       "self.TMC_GetSlopeDistCorr()",
                       "self.TMC_GetAngle1(%d)" % INC_MODE,
                       "self.TMC_GetSimpleMea(%d, %d)" % (WAIT_MEASURE, INC_MODE),
                       "self.TMC_GetSimpleCoord()",
                       "self.TMC_GetHeight()"]

        return self.do_dict(setter_dict=setter_dict,
                            getter_dict=getter_dict,
                            command_retry=command_retry,
                            command_wait=command_wait)

    def measure(self,
                HORIZONTAL_ANGLE=None,
                VERTICAL_ANGLE=None,
                REFLECTOR_HEIGHT=0.00,
                SEARCH_HORIZONTAL=1e-4,
                SEARCH_VERTICAL=1e-4,
                PRISM_TYPE=BAP.BAP_PRISM_MINI,
                POS_MODE=AUT.AUT_NORMAL,
                TMC_MODE=TMC.TMC_DEF_DIST,
                INC_MODE=TMC.TMC_AUTO_INC,
                FACE=0,
                FINE_ADJUST=False,
                WAIT_MEASURE=10000,
                position="TACHY-TPS-Position",
                targetName='TachyTarget',
                choice=2):
        """

        :param HORIZONTAL_ANGLE:
        :param VERTICAL_ANGLE:
        :param REFLECTOR_HEIGHT:
        :param SEARCH_HORIZONTAL:
        :param SEARCH_VERTICAL:
        :param PRISM_TYPE:
        :param POS_MODE:
        :param TMC_MODE:
        :param INC_MODE:
        :param FACE:
        :param FINE_ADJUST:
        :param WAIT_MEASURE:
        :param position:
        :param targetName:
        :param choice:
        :return:
        """
        if choice == 1:
            return self.measure1(HORIZONTAL_ANGLE=HORIZONTAL_ANGLE,
                                 VERTICAL_ANGLE=VERTICAL_ANGLE,
                                 REFLECTOR_HEIGHT=REFLECTOR_HEIGHT,
                                 SEARCH_HORIZONTAL=SEARCH_HORIZONTAL,
                                 SEARCH_VERTICAL=SEARCH_VERTICAL,
                                 PRISM_TYPE=PRISM_TYPE,
                                 TMC_MODE=TMC_MODE,
                                 INC_MODE=INC_MODE,
                                 FACE=FACE,
                                 FINE_ADJUST=FINE_ADJUST,
                                 WAIT_MEASURE=WAIT_MEASURE,
                                 position=position)

        elif choice == 2:
            return self.measure2(HORIZONTAL_ANGLE=HORIZONTAL_ANGLE,
                                 VERTICAL_ANGLE=VERTICAL_ANGLE,
                                 REFLECTOR_HEIGHT=REFLECTOR_HEIGHT,
                                 SEARCH_HORIZONTAL=SEARCH_HORIZONTAL,
                                 SEARCH_VERTICAL=SEARCH_VERTICAL,
                                 PRISM_TYPE=PRISM_TYPE,
                                 TMC_MODE=TMC_MODE,
                                 INC_MODE=INC_MODE,
                                 FACE=FACE,
                                 FINE_ADJUST=FINE_ADJUST,
                                 WAIT_MEASURE=WAIT_MEASURE,
                                 command_retry=3,
                                 command_wait=5)

    def measure1(self,
                HORIZONTAL_ANGLE=None,
                VERTICAL_ANGLE=None,
                REFLECTOR_HEIGHT=0.00,
                SEARCH_HORIZONTAL=1e-4,
                SEARCH_VERTICAL=1e-4,
                PRISM_TYPE=BAP.BAP_PRISM_MINI,
                # POS_MODE=AUT.AUT_NORMAL,
                TMC_MODE=TMC.TMC_DEF_DIST,
                INC_MODE=TMC.TMC_AUTO_INC,
                FACE=0,
                FINE_ADJUST=False,
                WAIT_MEASURE=10000,
                position="TACHY-TPS-Position",
                # targetName='TachyTarget'
                ):
        """
        Perform TACHY-TPS measurement.

        :type   HORIZONTAL_ANGLE    : float
        :param  HORIZONTAL_ANGLE    : Turn instrument to Hz [gon]
        :type   VERTICAL_ANGLE      : float
        :param  VERTICAL_ANGLE      : Turn instrument to Hz [gon]
        :type   REFLECTOR_HEIGHT    : float
        :param  REFLECTOR_HEIGHT    : Reflector Height
        :type   SEARCH_HORIZONTAL   : float
        :param  SEARCH_HORIZONTAL   : Search Window Hz [rad]
        :type   SEARCH_VERTICAL     : float
        :param  SEARCH_VERTICAL     : Search Window V [rad]
        :type   PRISM_TYPE          : int
        :param  PRISM_TYPE          : Prism Type
        :type   POS_MODE            : int
        :param  POS_MODE            : Positioning Mode (default = 0)
        :type   TMC_MODE            : int
        :param  TMC_MODE            : Measurement Mode (default = 0)
        :type   INC_MODE            : int
        :param  INC_MODE            : Inclination Mode (default = 1)
        :type   FACE                : int
        :param  FACE                : Face of TACHY (default = 0 [I])
        :type   FINE_ADJUST         : `bool <https://docs.python.org/2/library/functions.html#bool>`_
        :param  FINE_ADJUST         : Use AUT_FineAdjust (default = False)
        :type   WAIT_MEASURE        : int
        :param  WAIT_MEASURE        : Wait for TMC_GetSimpleMea in [ms] (default = 10000)

        :rtype: dict
        :return: TEMPERATURE, PPM, PRISM_CONSTANT, CROSS_INCLINE, LENGTH_INCLINE, HZ, V, SD or EMPTY
        """

        self._OUT = {}

        # Set Tachymeter
        try:
            TRY = True

            self.COM_NullProc()

            self.query()

            # self.TMC_DoMeasure(TMC.TMC_CLEAR)                     # Clean TPS data
            self.BAP_SetPrismType(PRISM_TYPE)                           # Set Prism Type
            self.TMC_SetHeight(REFLECTOR_HEIGHT)                        # Set Reflector Height

            if TRY:
                TRY = self.turn_to(HORIZONTAL_ANGLE=HORIZONTAL_ANGLE,
                                   VERTICAL_ANGLE=VERTICAL_ANGLE,
                                   SEARCH_HORIZONTAL=SEARCH_HORIZONTAL,
                                   SEARCH_VERTICAL=SEARCH_VERTICAL,
                                   FACE=FACE,
                                   FINE_ADJUST=FINE_ADJUST)

            # Get Tachymeter Output
            # print "CSV_GetIntTemp"
            if TRY:
                self._OUT.update(self.CSV_GetIntTemp())                     # Get TEMPERATURE
            # print "TMC_GetSlopeDistCorr"
                self._OUT.update(self.TMC_GetSlopeDistCorr())               # Get PPM, PRISM_CONSTANT
            # print "TMC_GetAngle1"
                self._OUT.update(self.TMC_GetAngle1(INC_MODE))              # Get CROSS_INCLINE, LENGTH_INCLINE
            # print "TMC_DoMeasure"
                TRY = self.TMC_DoMeasure(TMC_MODE, INC_MODE)                # Perform Measurement
            # print "TMC_GetSimpleMea"

            if TRY:
                self._OUT.update(self.TMC_GetFace())                        # Get FACE

            if TRY:
                self._OUT.update(self.TMC_GetSimpleMea(WAIT_MEASURE, INC_MODE))    # Get HORIZONTAL_ANGLE, VERTICAL_ANGLE, SLOPE_DISTANCE

# self._OUT.update(self.LG_GetAll())                        # Get All at the same time

                self._OUT.update(self.TMC_GetSimpleCoord())                 # Get EASTING, NORTHING, HEIGHT

                self._OUT.update(self.TMC_GetHeight())                      # Get REFLECTOR_HEIGHT

                self._OUT.update({'UID': GENERATES.gen_uuid(),
                                  'SYNCED': 0,
                                  'CREATED': GENERATES.gen_now(DATE_RETURN=True)})

            if TRY:
                if not self.ERRORCODE == "":
                    print "ERROR WHILE 'def measure()': %s" % self.ERRORCODE
                    return {}
                else:
                    # print self._OUT
                    return self._OUT
            else:
                return {}

        except ERROR.ConnectionError as e:
            raise ERROR.ConnectionError(sensorType="TACHY",
                                        sensorPosition=position)
        except ERROR.SensorRequestError as e:
            print e
            # print '%s: %s' % (inst.WHERE, inst.WHAT)
            return {}


# END
