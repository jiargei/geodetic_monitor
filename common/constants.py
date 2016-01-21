
# from constants_web import * # -> constants.RGB_COLOR
# import constants_web # -> constants.constants_web.RGB_COLOR

USER_ROLE_CHOICES = (
    ("u", "User"),
    ("m", "Manager"),
    ("a", "Admin"),
)

TARGET_TYPE_CHOICES = (
    ("d", "Deformationspunkt"),
    ("f", "Festpunkt"),
)

STATION_STABILISATION_CHOICE = (
    ('s', 'stable Station'),
    ('u', 'unstabile Station'),
)

ALARM_STATES = (
    (-2, "-ROT-"),
    (-1, "-ORANGE-"),
    (0, "+GRUEN+"),
    (1, "+ORANGE+"),
    (2, "+ROT+"),
)

SENSOR_TYPE_CHOICES = (
    (1, 'TACHY'),
    (2, 'METEO'),
    (3, 'DISTO'),
    (4, 'NIVEL')
)
