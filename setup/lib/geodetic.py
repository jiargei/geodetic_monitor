#!/bin/python

import math


def grid_to_polar(e1, n1, h1, e2, n2, h2):
    """
    2. Hauptaufgabe der Geodaesie.
    Wandelt Koordinaten in Beobachtungen.

    :param e1: Rechtswert vom Standpunkt
    :type e1: float
    :param n1: Hochwert vom Standpunkt
    :type n1: float
    :param h1: Hoehe vom Standpunkt
    :type h1: float
    :param e2: Rechtswert vom Zielpunkt
    :type e2: float
    :param n2: Hochwert vom Zielpunkt
    :type n2: float
    :param h2: Hoehe vom Zielpunkt
    :type h2: float
    :return: azimuth, zenith, distance
    :rtype: dict
    """
    azimuth = 0.

    de = e2-e1
    dn = n2-n1
    dh = h2-h1

    distance = math.sqrt(de**2 + dn**2 + dh**2)
    plane = math.sqrt(de**2 + dn**2)

    zenith = math.atan2(plane, dh)

    azimuth = math.atan2(de, dn)
    
    return {"azimuth": azimuth, "zenith": zenith, "distance": distance}


def polar_to_grid(e0, n0, h0, hz, ori, v, sd):
    """
    1. Hauptaufgabe der Geodaesie. 
    Wandelt Beobachtungen in Koordinaten.
    
    :param e0: Rechtswert vom Standpunkt
    :type e0: float
    :param n0: Hochwert vom Standpunkt
    :type n0: float
    :param h0: Hoehe vom Standpunkt
    :type h0: float
    :param hz: Richtungswinkel vom Stand- zum Zielpunkt in GON
    :type hz: float
    :param ori: Orientierung im Standpunkt in GON
    :type ori: float
    :param v: Vertikalwinkel vom Stand- zum Zielpunkt in GON
    :type v: float
    :param sd: Schraegdistanz vom Stand- zum Zielpunkt
    :type sd: float
    :return: easting, northing, height
    :rtype: dict
    """
    e1 = e0 + math.cos((hz+ori) * math.pi/200) * math.sin(v * math.pi/200) * sd
    n1 = n0 + math.sin((hz+ori) * math.pi/200) * math.sin(v * math.pi/200) * sd
    h1 = h0 + math.cos(v * math.pi/200) * sd
    
    return {"easting": e1, "northing": n1, "height": h1}

