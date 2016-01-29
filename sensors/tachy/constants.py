MODEL_TYPE_CHOICE = (
    (101, "Leica 1100-Series"),
    (102, "Leica 1200-Series"),
    (103, "Leica TS15"),
    (104, "Leica TM30"),
    (105, "Leica TM50"),
    (901, "Simulated Tachymeter"),
)

FACE_ONE = 0
FACE_TWO = 1
FACE_CHOICES = (
    (FACE_ONE, 'Lage I'),
    (FACE_TWO, 'Lage II'),
)

PRISM_CHOICES = (
    (0, "Leica Rundprisma"),
    (1, 'Leica Miniprisma'),
    (2, 'Leica Reflektorfolie'),
    (3, 'Leica 360'),
    (7, 'Leica Miniprisma 360'),
    (11, 'kein Prisma'),
)


class PrismConstant():
    PRISM_ROUND = 0.0
    PRISM_MINI = 0.0175
    PRISM_TAPE = 0.0344
    PRISM_360 = 0
    PRISM_MINI_360 = 0.0244
    PRISM_NONE = 0.0344

ON = 1
OFF = 0
