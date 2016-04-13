# -*- coding: utf-8 -*-

import math

from geodetic.calculations import convert
from geodetic.point import Point


def polar_to_grid(p1, azimut, zenith, distance):
    """
    1. Hauptaufgabe der Geodäsie... wandelt Richtungen und Strecken in Koordinaten um

    :param p1:
    :param azimut:
    :param zenith:
    :param distance:
    :return:
    """
    diff = Point(x=distance * math.sin(convert.gon2rad(azimut)) * math.sin(convert.gon2rad(zenith)),
                 y=distance * math.cos(convert.gon2rad(azimut)) * math.sin(convert.gon2rad(zenith)),
                 z=distance * math.cos(convert.gon2rad(zenith)))

    return p1.__add__(diff)


def grid_to_polar(p1, p2, orientation=0):
    """
    2. Hauptaufgabe der Geodäsie... wandelt ein Koordinaten paar in Richtungen und Strecken um

    :param p1: Standpunkt
    :param p2: Zielpunkt
    :param orientation: Orientierung
    :return:

    """
    DIFF = p2.__sub__(p1)
    # T_21 = convert.corr_hz(convert.rad2gon(math.atan2(DIFF.X, DIFF.Y))) + orientation
    T_21 = convert.rad2gon(math.atan2(DIFF.X, DIFF.Y)) + orientation
    SD_21 = p2.dist_slope(p1)
    SH_21 = p2.dist_plane(p1)
    Z_21_1 = convert.rad2gon(math.acos(DIFF.Z / SD_21))
    Z_21_2 = convert.rad2gon(math.atan2(SH_21, DIFF.Z))
    Z_21 = convert.corr_v((Z_21_1 + Z_21_2) / 2, 1)

    return {'azimut': T_21,
            'zenit': Z_21,
            'distanceSlope': SD_21,
            'distancePlane': SH_21}