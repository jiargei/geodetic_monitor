from django.db import models
from tachy_control.lib.constants import TACHY_TYPES

# Create your models here.

class TachySensor(models.Model):

    owner = models.ForeignKey('auth.User', related_name='tachysensors')
    instrument_name = models.CharField(max_length=50)
    instrument_number = models.CharField(max_length=50, primary_key=True)
    BAUD_14400 = 14400
    BAUD_19200 = 19200
    BAUD_9600 = 9600
    BAUD_4800 = 4800
    BAUDRATE_CHOICES = (
        (BAUD_4800, '4800'),
        (BAUD_9600, '9600'),
        (BAUD_14400, '14400'),
        (BAUD_19200, '19200'),
    )
    baudrate = models.PositiveSmallIntegerField(choices=BAUDRATE_CHOICES,
                                                default=BAUD_9600)

    BYTESIZE_AIGHT = 8
    BYTESIZE_SEVEN = 7
    BYTESIZE_CHOICES = (
        (BYTESIZE_AIGHT, '8'),
        (BYTESIZE_SEVEN, '7'),
    )
    bytesize = models.PositiveSmallIntegerField(choices=BYTESIZE_CHOICES,
                                                default=BYTESIZE_AIGHT)
    STOPBITS_ONE = 1
    STOPBITS_ZERO = 0
    STOPBITS_TWO = 2
    STOPBITS_CHOICES = (
        (STOPBITS_ONE, '1'),
        (STOPBITS_TWO, '2'),
        (STOPBITS_ZERO, '0'),
    )
    stopbits = models.PositiveSmallIntegerField(choices=STOPBITS_CHOICES,
                                                default=STOPBITS_ONE)
    device = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=2, default='FF')
    NONE = 'N'
    EVEN = 'E'
    ODD = 'O'
    PARITY_CHOICES = (
        (NONE, 'None'), (EVEN, 'Even'), (ODD, 'Odd')
    )
    parity = models.CharField(max_length=1,
                              choices=PARITY_CHOICES,
                              default=NONE)

    TACHY_CHOICES = (
        (TACHY_TYPES.LEICA_TPS11, 'Leica TPS1100'),
        (TACHY_TYPES.LEICA_TPS12, 'Leica TPS1200'),
        (TACHY_TYPES.FAKE_TACHY, 'Fake Tachymeter'),
        (TACHY_TYPES.LEICA_TS15, 'Leica TS15'),
        (TACHY_TYPES.LEICA_TS15_WITH_RADIOHANDLE, 'Leica TS15 with Radiohandle RH16'),
        (TACHY_TYPES.LEICA_TCA18, 'Leica TCA1800'),
    )
    model = models.PositiveSmallIntegerField(choices=TACHY_CHOICES,
                                             default=TACHY_TYPES.LEICA_TPS11)
