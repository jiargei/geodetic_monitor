# -*- coding: utf-8 -*-

#from dimosy.LIMIT import TYPES

LOG_FILE = "/var/www/dimosy/log/multi.log"

ENERGY_SAFE_MODE = False

DIRECT_PRINT = False

USE_VIS_LASER_FOR_MEASUREMENT = False

DEBUG_MODE = 0
COORDINATE_DIGITS = 4

MAX_NAME_LENGTH = 10

NOTIFICATION_EMAIL = 'watchdog@dimosy.com'
NOTIFICATION_SMS = '436643918692'

MULTI_WAIT_WINDOW = 7


#   _____          _                          _
#  |_   _|        | |                        | |
#    | | __ _  ___| |__  _   _ _ __ ___   ___| |_ ___ _ __
#    | |/ _` |/ __| '_ \| | | | '_ ` _ \ / _ \ __/ _ \ '__|
#    | | (_| | (__| | | | |_| | | | | | |  __/ ||  __/ |
#    \_/\__,_|\___|_| |_|\__, |_| |_| |_|\___|\__\___|_|
#                         __/ |
#                        |___/

# Zeitfenster, für jenes das Tachymeter eingeschalten bleiben soll, falls eine
# Folgemessung in genau diesem Zeitfenster passieren würde. Eingabe in Minuten.
TIME_WINDOW = 5
NULL_PRO_RETRY_TIME = 2
NULL_PRO_RETRY_ATTEMP = 6

SEARCH_VERTICAL = 1e-3
SEARCH_HORIZONTAL = 1e-3

SENSOR_SETTINGS = [{'TYPE_NAME': 'TACHY', 'TYPE_ID': 1, 'BAUDRATE': '9600', 'BYTESIZE': '8', 'STOPBITS': '1',
                    'PARITY': 'N'},
                   {'TYPE_NAME': 'NIVEL', 'TYPE_ID': 2, 'BAUDRATE': '9600', 'BYTESIZE': '8', 'STOPBITS': '1',
                    'PARITY': 'N'},
                   {'TYPE_NAME': 'METEO', 'TYPE_ID': 3, 'BAUDRATE': '4800', 'BYTESIZE': '8', 'STOPBITS': '1',
                    'PARITY': 'N'},
                   {'TYPE_NAME': 'DISTO', 'TYPE_ID': 4, 'BAUDRATE': '19200', 'BYTESIZE': '7', 'STOPBITS': '1',
                    'PARITY': 'E'}]


# ORIENTERIUNG
ORIENTATION_MAX_DIFFERENCE = 0.0100

# PROJECT
PROJECT_TYPE_LIST = ["test", "demo", "real"]
PROJECT_TYPE = "test"
SCREEN_STANDARD = "desktop"

# PLAUSIBILITÄTSCHECK [m]
MAX_PERP_LR = 0.3
MAX_PERP_UD = 0.3
MAX_DISTANCE = 0.3

# WIEDERHOLUNGEN FÜR PointOperation Wiederholungen
POINT_OPERATION_RETRIES = 1

# Systemlimits
