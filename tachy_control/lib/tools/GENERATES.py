# -*- coding: utf-8 -*-

import uuid
import sys
import re
import datetime
import time


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def __init__(self):
        pass

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
        
        
def read_d40(s1):
    """
    Funktion um das Dateiformat D40 einlesen zukönnen.
    
    Die Datenart "040" beschreibt einen Achsverlauf im Grundriss.
    Je Datensatz wird ein Bogenhauptpunkt beschrieben.
    Die Dimensionen sind [m] bzw. [gon] mit Dezimalpunkt.
    Es wird das geodätische Koordinatensystem (Y ist Rechtswert, X der Hochwert) 
    verwendet.

    :param s1:
    
    :rtype: list
    :return: Liste von Achssegmenten
    """
    
    """    
    *** Datenart
       ** Achsbezeichnung
         ********** Station Bogenhauptpunkt   
                   ******** Bogenlänge des ankommenden Achselementes   
                           ************ Radius am Bogenanfang   
                                       ********* Klotoidenparameter   
                                                ************ Tangentenrichtung
                                                            ************ Y
                                                                        ************ X
    040 1 13646.993   0.000      0.0000    0.000 243.9050677  491257.062  624934.794
    040 1 14747.8861100.893     -0.0001  750.000 243.9050677  490556.592  624085.496
    040 1 15029.136 281.250  -2000.0000    0.000 239.4288349  490382.812  623864.437
    040 1 15292.375 263.239  -2000.0000 -500.000 231.0496666  490244.527  623640.669
    040 1 15417.375 125.000      0.0000    0.000 229.0602298  490188.266  623529.052
    040 1 16916.1471498.772      0.0000    0.000 229.0602298  489527.624  622183.738
    040 2     0.000   0.000    501.7500    0.000 265.4119997  494320.117  624859.382
    040 2     7.015   7.015    -12.0000    0.000 266.3020368  494314.087  624855.798
    """
    
    d40 = []
    for zeile in s1.split('\n'):
        m = re.match(r"(?P<datenart>[0-9]{3})(?P<achsbezeichnung>[\w]{2})(?P<station>([ ]*[-+]?[ \d]{0,10}[.]?\d{0,3}))(?P<bogenlaenge>[ ]*[-+]?\d{0,8}[.]?\d{0,3})(?P<radius>[ ]*[-+]?\d{0,12}[.]?\d{0,11})(?P<klothoide>[ ]*[-+]?\d{0,9}[.]?\d{0,3})(?P<tangente>[ ]*\d{0,12}[.]?\d{0,7})(?P<rechts>[ ]*[+-]?\d{0,12}[.]?\d{0,3})(?P<hoch>[ ]*[-+]?\d{0,12}[.]\d{0,3})", zeile)
      
        if m:
            Format = m.group("datenart")
            Achse = m.group("achsbezeichnung")
            Station = m.group("station")
            Laenge = m.group("bogenlaenge")
            Radius = m.group("radius")
            Klotho = m.group("klothoide")
            Tangent = m.group("tangente")
            RW = m.group("rechts")
            HW = m.group("hoch")
            
# if (not zeile[0]=='#') and (len(zeile)>=80):
#             Format = zeile[0:3]
#             Achse  = zeile[3:5]
#             Station= zeile[5:15]
#             Laenge = zeile[15:23]
#             Radius = zeile[23:35]
#             Klotho = zeile[35:44]
#             Tangent= zeile[44:56]
#             RW     = zeile[56:68]
#             HW     = zeile[68:80]
        
            d40.append({'FORMAT': Format,
                        'ACHSE': Achse,
                        'STATION': float(Station),
                        'LAENGE': float(Laenge),
                        'RADIUS': float(Radius),
                        'KLOTHOIDE': float(Klotho),
                        'TANGENTE': float(Tangent),
                        'EASTING': float(RW),
                        'NORTHING': float(HW)})
            
    return d40
        

def calc_checksum(converter):
    """
    Berechent die Prüfsumme für einen String und gibt diese im HEX-Format
    zurück.

    :type converter: str
    :param converter: Prüfsummenstring

    :rtype: str
    :return: Prüfsumme im hexadezimal Format
    """
    checksum = 0
    for i in converter:
        checksum = checksum + ord(i)
    return "{:02x}".format(checksum).upper()[-2:]


def check_float(value, LEVEL="DiMoSy", allowNegative=True):
    """
    Checks a value for against type float.
    
    :type value: float
    :param value: value to be checked against float type
    :type allowNegative: `bool <https://docs.python.org/2/library/functions.html#bool>`_
    :param allowNegative: If True, negative values will be accepted
    
    :rtype: `bool <https://docs.python.org/2/library/functions.html#bool>`_
    :return: Checks if type is float (True) else (False)
    """
    
    try:
        if isinstance(float(value), float):
            if not allowNegative and value < 0.0:
                return False
            else:
                return True
#         elif isinstance(value)==type(None):
#             print "|%15s|%-20s @ %-38s |" % (gen_now("%Y%m%d-%H%M%S"),LEVEL,"Leere Eingabe")
#             return False
    except:
        print "|%15s|%-20s @ %-38s |" % (gen_now("%Y%m%d-%H%M%S"), LEVEL, "Fehlerhafte Eingabe")
        return False
        
    
def set_float(value=None, axis="DiMoSy", default=0.0, pre_check=False, allowNegative=True, SCREEN="desktop"):
    """
    Setting a float value using the check function check_float()
    
    :type value: float
    :param value: Value to check
    :type axis: str
    :param axis: What kind of value (easting, northing, ...)
    :type default: float
    :param default: default for value
    :type pre_check: `bool <https://docs.python.org/2/library/functions.html#bool>`_
    :param pre_check: If pre_check is true, value will be set automatically
    :type allowNegative: `bool <https://docs.python.org/2/library/functions.html#bool>`_
    :param allowNegative: If True, negative Values will be accepted
    
    :rtype: float
    :return: returns a float type value
    """
    
    if pre_check:
        raw_value = value
        if (value == None or value == ''):
            raw_value = default
        _is_set = check_float(raw_value, axis)
    else:
        _is_set = False
        raw_value = None

    while not _is_set:
        if SCREEN == "desktop":
            sys.stdout.write(bcolors.FAIL + "|%s%-21s" % (" " * 16, "%s [%.1f]" % (axis.decode("utf-8"), default)))
        if SCREEN == "mobile":
            sys.stdout.write(bcolors.FAIL + "%s [%.1f]" % (axis.decode("utf-8"), default))

        raw_value = raw_input(": " + bcolors.ENDC)

        if raw_value is None or raw_value == '':
            raw_value = default

        _is_set = check_float(raw_value, axis)

    return float(raw_value)


def user_interact(CHOICE_LIST=[], PRE_CHOICE='', USER_CHOICE=None, Eingabe="Auswahl", SCREEN="desktop"):
    """
    Performs a user interaction referring to a defined list. The procedure loops
    as long as no possible choice was made.
        
    :type   CHOICE_LIST: list[str]
    :param  CHOICE_LIST: possible answers for user interaction
    :type   USER_CHOICE: int, float, string
    :param  USER_CHOICE: premade choice (for automatisation)
    :type   PRE_CHOICE: int,float,string
    :param  PRE_CHOICE: default choice (Hit Enter to get it)
    :type   Eingabe: str
    :param  Eingabe: Text for raw_input()
    
    :rtype: str
    :return: one of the possible choices
    """
    SHOW_CHOICE = ' [%s]' % PRE_CHOICE if not PRE_CHOICE == '' else ''
    
    if not CHOICE_LIST:
        if SCREEN == "desktop":
            USER_CHOICE = raw_input(bcolors.FAIL + "%sWeiter mit ENTER ... " % ("|" + " " * 16) + bcolors.ENDC)
        if SCREEN == "mobile":
            USER_CHOICE = raw_input(bcolors.FAIL + " Weiter mit ENTER > " + bcolors.ENDC)
    else:
        while not USER_CHOICE in CHOICE_LIST:
            if SCREEN == "desktop":
                USER_CHOICE = raw_input(bcolors.FAIL + "\n%s%-21s: " % ("|" + " " * 16,
                                                                        Eingabe + SHOW_CHOICE) + bcolors.ENDC)
            if SCREEN == "mobile":
                USER_CHOICE = raw_input(bcolors.FAIL + "%s: " % (Eingabe + SHOW_CHOICE) + bcolors.ENDC)
            if USER_CHOICE == "" or not USER_CHOICE:
                USER_CHOICE = PRE_CHOICE
    return USER_CHOICE


def user_value(v=None, t=float):
    """

    :param v:
    :param t:
    :return:
    """
    _is_set = False
    while not _is_set:
        if v and isinstance(v, t):
            _is_set = True
            return v
        elif v and not isinstance(v, t):
            pass
        ### not finished
        

def gen_uuid():
    """
    Generates an UUID using uuid.uuid4()

    :rtype: str
    :return: UUID
    """
    return "%s" % uuid.uuid4()


def gen_string(eingabeText="Zu setzende Variable", eingabeWert="", SCREEN="desktop"):
    """

    :param eingabeText:
    :param eingabeWert:
    :param SCREEN:
    :return:
    """
    newString = ""
    
    while newString == "":
        showChoice = ' [%s]' % eingabeWert if not eingabeWert == '' else ''
        if SCREEN == "desktop":
            newString = raw_input(bcolors.FAIL + "\n%s%-21s: " % ("|" + " " * 16,
                                                                  eingabeText + showChoice) + bcolors.ENDC)
        if SCREEN == "mobile":
            newString = raw_input(bcolors.FAIL + "\n%s %s: " % (eingabeText, showChoice) + bcolors.ENDC)
        if newString == "":
            newString = eingabeWert
    return newString


def gen_now(sf="%Y-%m-%d %H:%M:%S", DATE_RETURN=False, DATE=None):
    """
    Liefert ein Datum als Antwort als String im Format 'sf'.
    Bei DATE_RETURN=True wird als Ergebnis ein Typ datetime.datetime als Antwort gegeben.
    
    :type sf: str
    :param sf: date format %Y,%m, ...
    :type DATE_RETURN: `bool <https://docs.python.org/2/library/functions.html#bool>`_
    :param DATE_RETURN: if set True return changes from string to datetime.datetime
    
    :rtype: str, datetime.datetime
    :return: datetime as string or type
    """
    if not DATE:
        DATE = datetime.datetime.now().strftime(sf)
    
    if DATE_RETURN:
        return datetime.datetime.strptime(DATE, sf)
    else:
        return DATE

    
def gen_time(hour=0, minute=0, second=0, milli_seconds=1):
    """
    Erzeugt eine Zeit

    :param hour: Stunden
    :type hour: int
    :param minute: Minuten
    :type minute: int
    :param second: Sekunden
    :type second: int
    :param milli_seconds: Millisekunden
    :type milli_seconds: float
    :return: Zeit
    :rtype: datetime.time
    """
    return datetime.time(hour, minute, second, milli_seconds)


def check_time_window(timeNow=None, timeInterval=60, timeWindow=5):
    """
    Überprüft, ob das aktuelle Datum innerhalb eines Zeitfensters liegt. Dabei
    wird als Ausgangszeit 00:00:00 herangezogen.
    
    :type timeNow: datetime.datetime
    :param timeNow: Datum, welches zu überprüfen ist
    :type timeInterval: float
    :param timeInterval: Zeitintervall in Minuten
    :type timeWindow: int
    :param timeWindow: Zeitfenster in Minuten
    
    :rtype: `bool <https://docs.python.org/2/library/functions.html#bool>`_
    :return: True, wenn Zeit innerhalb des Zeitfensters liegt, sonst False
    """
    if not timeNow:
        timeNow = gen_now(DATE_RETURN=True)
    
    timeNow = time_to_sec(timeNow)
    nextMeasurement = timeNow % (timeInterval * 60)
            
    return nextMeasurement < timeWindow * 60


def time_to_sec(dateTime):
    """
    Wandelt ein datetime.datetime in Sekunden um. Dabei wird das Datum nicht
    brücksichtigt und lediglich die Uhrzeit verarbeitet.
    
    :type dateTime: datetime.datetime
    :param dateTime: datetime, welches in Sekunden des Tages umgewandelt werden
    
    :rtype: int
    :return: Anzahl der Sekunden von dateTime bezogen auf die Uhrzeit
    """
    return dateTime.hour * 3600 + dateTime.minute * 60 + dateTime.second


def datetime_to_sec(dateTime):
    """
    Wandelt ein datetime.datetime in Sekunden um. Dabei wird nur das Datum sowie 
    die Uhrzeit berücksichtigt.
    
    :type dateTime: datetime.datetime
    :param dateTime: Datum, dass in Sekunden umgewandelt werden soll
        
    :rtype: int
    :return: Anzahl der Sekunden von dateTime bezogen auf Datum und Uhrzeit
    """
    
    if isinstance(dateTime, datetime.datetime):
        return int(time.mktime(dateTime.timetuple()))
    
    elif isinstance(dateTime, str):
        return int(time.mktime(datetime.datetime.strptime(dateTime, "%Y-%m-%d %H:%M:%S").timetuple()))

    elif isinstance(dateTime, int):
        return dateTime

    else:
        return -1

    
def conv_dict(DATA):
    for COLUMN in DATA:
        if isinstance(DATA[COLUMN], str):                           # check if its a string
            # print "%25s = %s" % (COLUMN,type(DATA[COLUMN]))
            DATA[COLUMN] = conv_dict_str(DATA, COLUMN)
            
        elif isinstance(DATA[COLUMN], datetime.datetime):           # check if its a datetime.datetime
            # print "%25s = %s" % (COLUMN,type(DATA[COLUMN]))
            DATA[COLUMN] = conv_dict_date(DATA, COLUMN)
            
        elif isinstance(DATA[COLUMN], datetime.time):               # check if its a datetime.time
            # print "BEFORE.. %25s = %s" % (COLUMN,type(DATA[COLUMN])), DATA[COLUMN]
            DATA[COLUMN] = conv_dict_time(DATA, COLUMN)
            # print "AFTER... %25s = %s" % (COLUMN,type(DATA[COLUMN])), DATA[COLUMN]
            
        elif isinstance(DATA[COLUMN], datetime.timedelta):          # check if its a datetime.timedelta
            # print "%25s = %s" % (COLUMN,type(DATA[COLUMN]))
            DATA[COLUMN] = conv_dict_timedelta(DATA, COLUMN)
            
        elif isinstance(DATA[COLUMN], int):
            # print "%25s = %s" % (COLUMN,type(DATA[COLUMN]))
            DATA[COLUMN] = DATA[COLUMN]
            
        elif isinstance(DATA[COLUMN], float):
            # print "%25s = %s" % (COLUMN,type(DATA[COLUMN]))
            DATA[COLUMN] = conv_float(DATA[COLUMN])
            
        elif DATA[COLUMN] is None:                                  # check if its a NoneType
            # print "%25s = %s" % (COLUMN,type(DATA[COLUMN]))
            DATA[COLUMN] = 'NULL'
        
        else:
            # print "%25s = %s ???" % (COLUMN,type(DATA[COLUMN]))
            DATA[COLUMN] = DATA[COLUMN]
    return DATA


def check_name(self, Value, Table, Project):
        """
        :type Value: str
        :param Value: Punktnummer
        :type Table: str
        :param Table: Tabellenname
        :type Project: str
        :param Project: Project UID
        :rtype: `bool <https://docs.python.org/2/library/functions.html#bool>`_
        :return: Not NULL and not in DB (True) else (False)
        """
        
        TRY = self.QUERY.FETCH("SELECT SUM('%s' LIKE tc.NAME) FROM %s AS tc WHERE PROJECT_UID='%s'",
                               (Value, Table, Project), ROWS=1)
        if not TRY[0] == 0:
            print "|%15s|%-20s @ %-38s |" % (gen_now("%Y%m%d-%H%M%S"), "COORDINATE", "Punktnummer bereits vergeben")
            return False
        elif not Value:
            print "|%15s|%-20s @ %-38s |" % (gen_now("%Y%m%d-%H%M%S"), "COORDINATE", "Punktnummer darf nicht leer sein")
            return False
        else:
            return True
        

def set_name(self, value=None, name="Name"):
    """
    Assigns a Name for the Coordinate

    :param value:
    :param name:
    :return:
    """
    #_is_set = self.check_name(value)
    # while not _is_set:
    while not value:
        value = raw_input("%-20s: " % name)
        value = value if self.check_name(value) else ""

        #_is_set = self.check_name(value)

    #value = raw_input("%-20s: " % "Name")
    self.__NAME = value


def conv_float(FLOAT, PRECISION=6):
    """

    :param FLOAT:
    :param PRECISION:
    :return:
    """
    return round(FLOAT, PRECISION)


def conv_timedelta(TIMEDELTA, AS_STRING=True):
    """

    :param TIMEDELTA:
    :param AS_STRING:
    :return:
    """
    # print TIMEDELTA.seconds
    H = TIMEDELTA.seconds / 60 / 60
    M = (TIMEDELTA - datetime.timedelta(0, 0, 0, 0, 0, H, 0)).seconds / 60
    S = (TIMEDELTA - datetime.timedelta(0, 0, 0, 0, M, H, 0)).seconds
    return datetime.time(H, M, S, 1).strftime("'%H:%M:%S'") if AS_STRING \
        else datetime.time(H, M, S, 1)


def conv_dict_timedelta(DATA, COLUMN):
    """

    :param DATA:
    :param COLUMN:
    :return:
    """
    return 'NULL' if (not COLUMN in DATA) else 'NULL' if not DATA[COLUMN] \
        else conv_timedelta(DATA[COLUMN])


def conv_date(DATE, sf="'%Y-%m-%d %H:%M:%S'"):
    """

    :param DATE:
    :param sf:
    :return:
    """
    return DATE.strftime(sf)
    

def conv_dict_date(DATA, COLUMN):
    """

    :param DATA:
    :param COLUMN:
    :return:
    """
    return conv_date(DATA[COLUMN]) if (COLUMN in DATA and DATA[COLUMN]) \
        else gen_now(sf="'%Y-%m-%d %H:%M:%S'", DATE_RETURN=False)


def conv_time(TIME):
    """

    :param TIME:
    :return:
    """
    return TIME.strftime("'%H:%M:%S'")


def conv_dict_time(DATA, COLUMN):
    """

    :param DATA:
    :param COLUMN:
    :return:
    """
    return 'NULL' if (not COLUMN in DATA) else 'NULL' if not DATA[COLUMN] \
        else conv_time(DATA[COLUMN])


def conv_str(STRING):
    """

    :param STRING:
    :return:
    """
    return "'" + STRING + "'"


def conv_dict_str(DATA, COLUMN):
    """

    :param DATA:
    :param COLUMN:
    :return:
    """
    return 'NULL' if (not COLUMN in DATA) else 'NULL' if not DATA[COLUMN] \
        else conv_str(DATA[COLUMN])


def increment_PNo(curno):
    """
    Increments the Point Number via RegExp
    :param curno: current Pointnumber
    :return: next Pointnumber
    """
    pattern = re.compile(r"(?P<num>\d+$)")
    res = pattern.search(curno)
    if res:
        pre = curno[:res.start("num")]
        post = res.group("num")
        postinc = str(int(post)+1)
        zeros = "0"*(len(post)-len(postinc))
        return pre+zeros+postinc
    else:
        return curno+"2"