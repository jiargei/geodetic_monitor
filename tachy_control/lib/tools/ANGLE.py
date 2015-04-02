# -*- coding: utf-8 -*-

import math

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


def corr_hz(angle, UNIT='gon', EPS=5e-6):
    """
    Korrigiert den Hz-Winkel in der gewünschten Einheit.

    :param angle: Eingangswinkel Hz [UNIT]
    :type angle: float
    :param UNIT: Einheit
    :type UNIT: str
    :param EPS:
    :type EPS: float

    :return: korrigierter Hz-Winkel [UNIT]
    :rtype: float
    """
    if UNIT == 'gon':
        CIRCLE = 400
    elif UNIT == 'rad':
        CIRCLE = 2 * math.pi
        EPS = gon2rad(EPS)
    elif UNIT == 'grad':
        CIRCLE = 360;
    else:
        pass
    
    while angle < 0:
        angle += CIRCLE
    while angle >= CIRCLE:
        angle -= CIRCLE
    
    if abs(CIRCLE - angle) <= EPS:
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
    
    
def kreis_ablage(M, A, P, r):
    """
    Berechnet die Ablage eines Punktes auf einen Kreisbogen der bei A beginnt
    und den Radius r besitzt.
    
    Die Punkte A,M,P werden in Form von dict eingelesen {'EASTING': ..., ...}
    und als Ergebnis erhält man ein dict mit {'QUER': ..., 'LAENGS': ...}
    
    :rtype: dict
    :return: QUER, LAENGS
    """

    b = math.sqrt((M['EASTING'] - P['EASTING']) ** 2 + (M['NORTHING'] - P['NORTHING']) ** 2)
    a = math.sqrt((M['EASTING'] - A['EASTING']) ** 2 + (M['NORTHING'] - A['NORTHING']) ** 2)
    c = math.sqrt((A['EASTING'] - P['EASTING']) ** 2 + (A['NORTHING'] - P['NORTHING']) ** 2)

    w = math.acos((c ** 2 - a ** 2 - b ** 2) / (-2 * a * b))

    l = w * r
    q = b - r
    
    return {'QUER': q,
            'LAENGS': l}