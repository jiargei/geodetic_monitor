#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
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

OBSERVATION_UNIT_CHOICES = (
    ('m', 'Meter'),
    ('dm', 'Dezimeter'),
    ('cm', 'Zentimeter'),
    ('mm', 'Millimeter'),
    ('gon', 'Gon'),
    ('mgon', 'Milligon')
)

OBSERVATION_TYPE_CHOICES = (
    ('dH', u'Höhenänderung'),
    ('dE', u'Änderung Rechtswert'),
    ('dN', u'Änderung Hochwert'),
    ('dl', u'Längsverschiebung'),
    ('dq', u'Querverschiebung'),
    ('dS', u'Streckenänderung'),
    ('dHz', u'Änderung Horizontalwinkel'),
    ('dV', u'Änderung Vertikalwinkel'),
)

STATUS_ACTIVE = 16
STATUS_INACTIVE = 0

STATUS_CHOICES = (
    (STATUS_ACTIVE, _('active')),
    (STATUS_INACTIVE, _('inactive'))
)

TASK_CATEGORY_CHOICES = (
    ('m', 'Simple Measurement'),
    ('c', 'Control Measurement'),
    ('r', 'Resection')
)