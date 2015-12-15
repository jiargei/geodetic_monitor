
USER_ROLE_CHOICES = (
    ("u", "User"),
    ("m", "Manager"),
    ("a", "Admin"),
)

PRISM_CHOICES = (
        (1, 'Miniprisma'),
        (7, 'Miniprisma 360'),
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

LIMIT_STATES = (
    (-2, "ROT-"),
    (-1, "ORANGE-"),
    (0, "GRUEN"),
    (1, "ORANGE+"),
    (2, "ROT+"),
)