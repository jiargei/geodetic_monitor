
# from constants_web import * # -> constants.RGB_COLOR
# import constants_web # -> constants.constants_web.RGB_COLOR

USER_ROLE_CHOICES = (
    ("u", "User"),
    ("m", "Manager"),
    ("a", "Admin"),
)

PRISM_CHOICES = (
    (0, "Leica Rundprisma"),
    (1, 'Leica Miniprisma'),
    (2, 'Leica Reflektorfolie'),
    (3, 'Leica 360'),
    (7, 'Leica Miniprisma 360'),
    (11, 'kein Prisma')
)

TARGET_TYPE_CHOICES = (
    ("d", "Deformationspunkt"),
    ("f", "Festpunkt"),
)

FACE_ONE = 0
FACE_TWO = 1
FACE_CHOICES = (
    (FACE_ONE, 'Lage I'),
    (FACE_TWO, 'Lage II'),
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
