# -*- coding: utf-8 -*-

import math
from geodetic.point import Point


def rad2gon(angle):
    """
    :type angle: float
    :param angle: Winkel [rad].
    :rtype: float
    :return: liefert den Winkel [gon]
    """
    # angle_gon = angle * 200 / math.pi
    # while angle_gon >= 400:
    #     angle_gon -= 400
    # return corr_hz(angle_gon)

    return corr_hz(angle * 200 / math.pi)


def gon2rad(angle):
    """
    :type angle: float
    :param angle: Winkel [gon].
    :rtype: float
    :return: liefert den Winkel [rad]
    """
    return angle * math.pi / 200


def corr_hz(angle, unit='gon', eps=5e-6):
    """
    Korrigiert den Hz-Winkel in der gewünschten Einheit.

    :param angle: Eingangswinkel Hz [unit]
    :type angle: float
    :param unit: Einheit
    :type unit: str
    :param eps:
    :type eps: float

    :return: korrigierter Hz-Winkel [unit]
    :rtype: float
    """
        
    if unit == 'rad':
        circle = 2 * math.pi
        eps = gon2rad(eps)
    elif unit == 'grad':
        circle = 360
    else:
        circle = 400

    while angle < 0:
        angle += circle
    while angle >= circle:
        angle -= circle
    
    if abs(circle - angle) <= eps:
        angle = 0

    return angle


def corr_v(angle, face):
    return angle


def change_face_hz(angle, face=0):
    """
    Berechnet den Hz-Winkel in der gewünschten Lage

    :type angle: float
    :param angle: Eingangswinkel Hz [gon]
    :type face: int
    :param face: gewünschte Lage (default = 0 [I])

    :rtype: float
    :return: Korrigierter Hz-Winkel [gon]
    """
    if face == 1:
        return angle - 200 if angle >= 200 else angle + 200
    elif face == 0:
        return angle
    
    
def change_face_v(angle, face=0):
    """
    Berechnet den V-Winkel in der gewünschten Lage

    :type angle: float
    :param angle: Eingangswinkel V [gon]
    :type face: int
    :param face: gewünschte Lage (default = 0 [I])

    :rtype: float
    :return: Korrigierter V-Winkel [gon]
    """
    
    if face == 1:
        return 400 - angle
    elif face == 0:
        return angle
    
    
def kreis_ablage(m, a, p, r):
    """
    Berechnet die Ablage eines Punktes auf einen Kreisbogen mit Mittelpunkt m,
    der bei a beginnt und den Radius r besitzt.

    :type m: Point
    :type a: Point
    :type p: Point
    
    :rtype: dict
    :return: cross, length
    """

    b = math.sqrt((m.x - p.x) ** 2 + (m.y - p.y) ** 2)
    a = math.sqrt((m.x - a.x) ** 2 + (m.y - a.y) ** 2)
    c = math.sqrt((a.x - p.x) ** 2 + (a.y - p.y) ** 2)

    w = math.acos((c ** 2 - a ** 2 - b ** 2) / (-2 * a * b))

    r = a - m
    r = r.norm2D()

    l = w * r
    q = b - r
    
    return {'cross': q,
            'length': l}
