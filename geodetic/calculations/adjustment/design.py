# -*- coding: utf-8 -*-

import numpy


def dRdX(pi, pk):
    return float(1 * (pi.y - pk.y) / (numpy.sqrt((pi.x - pk.x) ** 2 + (pi.y - pk.y) ** 2)) ** 2)
    # return float(-(Pi.y - Pk.y)/(Pi.x**2 - 2*Pi.x*Pk.x + Pk.x**2 + (Pi.y - Pk.y)**2))


def dRdY(pi, pk):
    return float(-1 * (pi.x - pk.x) / (numpy.sqrt((pi.x - pk.x) ** 2 + (pi.y - pk.y) ** 2)) ** 2)
    # return float( (Pi.x - Pk.x)/(Pi.y**2 - 2*Pi.y*Pk.y + Pi.x**2 - 2*Pi.x*Pk.x + Pk.x**2 + Pk.y**2) )


def dRdO(pi, pk):
    return 1


def dSdX(pi, pk):
    return float((pi.x - pk.x) / numpy.sqrt((pi.x - pk.x) ** 2 + (pi.y - pk.y) ** 2))
    # return float((1.0*Pi.x - 1.0*Pk.x)*((-Pi.x + Pk.x)**2 + (-Pi.y + Pk.y)**2 + (-Pi.z + Pk.z)**2)**(-0.5))


def dSdY(pi, pk):
    return float((pi.y - pk.y) / numpy.sqrt((pi.x - pk.x) ** 2 + (pi.y - pk.y) ** 2))
    # return float((1.0*Pi.y - 1.0*Pk.y)*((-Pi.x + Pk.x)**2 + (-Pi.y + Pk.y)**2 + (-Pi.z + Pk.z)**2)**(-0.5))


def dSdO(pi, pk):
    return 0


def design_2d(pi, pk):
    """
    Liefert die Design-Matrix für ein einen Standpunkt und Zielpunkt.

    :type   pi                  : Point
    :param  pi                  : Standpunkt
    :type   pk                  : Point
    :param  pk                  : Zielpunkt
    :rtype: numpy.array
    :return: Desingmatrix für Zielpunkt Pk und Standpunkt Pi
    """

    "partial derivatives Distance"
    # dS_dxi = (1.0*Pi.x - 1.0*Pk.x)*((-Pi.x + Pk.x)**2 + (-Pi.y + Pk.y)**2 + (-Pi.z + Pk.z)**2)**(-0.5)
    # dS_dyi = (1.0*Pi.y - 1.0*Pk.y)*((-Pi.x + Pk.x)**2 + (-Pi.y + Pk.y)**2 + (-Pi.z + Pk.z)**2)**(-0.5)
    # dS_dzi = (1.0*Pi.z - 1.0*Pk.z)*((-Pi.x + Pk.x)**2 + (-Pi.y + Pk.y)**2 + (-Pi.z + Pk.z)**2)**(-0.5)
    # dS_doi = 0

    "partial derivatives Azimuth"
    # dR_dxi = -(-Pi.y + Pk.y)/((-Pi.x + Pk.x)**2 + (-Pi.y + Pk.y)**2) # dx/dy
    # dR_dyi = -(Pi.x - Pk.x)/((-Pi.x + Pk.x)**2 + (-Pi.y + Pk.y)**2)  #dx/dy

    # dR_dxi = -(Pi.y - Pk.y)/((-Pi.x + Pk.x)**2 + (-Pi.y + Pk.y)**2) # dy/dx
    # dR_dyi = -(-Pi.x + Pk.x)/((-Pi.x + Pk.x)**2 + (-Pi.y + Pk.y)**2) # dy/dx

    # dR_dxi = -1/((-Pi.y + Pk.y)*((-Pi.x + Pk.x)**2/(-Pi.y + Pk.y)**2 + 1))
    # dR_dyi = (-Pi.x + Pk.x)/((-Pi.y + Pk.y)**2*((-Pi.x + Pk.x)**2/(-Pi.y + Pk.y)**2 + 1))
    # dR_dzi = 0
    # dR_doi = -1

    "partial derivatives Zenith"
    # dZ_dxi = (1.0*Pi.x - 1.0*Pk.x)*(-Pi.z + Pk.z)*((-Pi.x + Pk.x)**2 + (-Pi.y + Pk.y)**2)**(-0.5)/((-Pi.z + Pk.z)**2 + ((-Pi.x + Pk.x)**2 + (-Pi.y + Pk.y)**2)**1.0)
    # dZ_dyi = (1.0*Pi.y - 1.0*Pk.y)*(-Pi.z + Pk.z)*((-Pi.x + Pk.x)**2 + (-Pi.y + Pk.y)**2)**(-0.5)/((-Pi.z + Pk.z)**2 + ((-Pi.x + Pk.x)**2 + (-Pi.y + Pk.y)**2)**1.0)
    # dZ_dzi = ((-Pi.x + Pk.x)**2 + (-Pi.y + Pk.y)**2)**0.5/((-Pi.z + Pk.z)**2 + ((-Pi.x + Pk.x)**2 + (-Pi.y + Pk.y)**2)**1.0)

    # dZ_dxi = (1.0*Pi.x - 1.0*Pk.x)*((-Pi.x + Pk.x)**2 + (-Pi.y + Pk.y)**2)**(-0.5)/((1 + ((-Pi.x + Pk.x)**2 + (-Pi.y + Pk.y)**2)**1.0/(-Pi.z + Pk.z)**2)*(-Pi.z + Pk.z))
    # dZ_dyi = (1.0*Pi.y - 1.0*Pk.y)*((-Pi.x + Pk.x)**2 + (-Pi.y + Pk.y)**2)**(-0.5)/((1 + ((-Pi.x + Pk.x)**2 + (-Pi.y + Pk.y)**2)**1.0/(-Pi.z + Pk.z)**2)*(-Pi.z + Pk.z))
    # dZ_dzi = ((-Pi.x + Pk.x)**2 + (-Pi.y + Pk.y)**2)**0.5/((1 + ((-Pi.x + Pk.x)**2 + (-Pi.y + Pk.y)**2)**1.0/(-Pi.z + Pk.z)**2)*(-Pi.z + Pk.z)**2)
    # dZ_doi = 0

    # return numpy.array([[float(dR_dxi), float(dR_dyi), float(dR_dzi)],
    #                     [float(dZ_dxi), float(dZ_dyi), float(dZ_dzi)],
    #                     [float(dS_dxi), float(dS_dyi), float(dS_dzi)]])
    # return numpy.array([[float(dR_dxi), float(dR_dyi), float(dR_dzi), float(dR_doi)],
    #                     [float(dZ_dxi), float(dZ_dyi), float(dZ_dzi), float(dZ_doi)],
    #                     [float(dS_dxi), float(dS_dyi), float(dS_dzi), float(dS_doi)]])

    return numpy.array([[dRdX(pi, pk), dRdY(pi, pk), dRdO(pi, pk)],
                        [dSdX(pi, pk), dSdY(pi, pk), dSdO(pi, pk)]])


def dVdZ(pi, pk):
    """
    partial derivative of zenit to height
    :param pi: station
    :param pk: target
    """
    sd = pk.dist_slope(pi)
    sh = pk.dist_plane(pi)
    return float((sh ** 2) * (sd ** 2) ** (-1.5) * numpy.sqrt((sh ** 2) / (sd ** 2)))


def design_1d(station, target):
    """
    
    Args:
        station: station
        target: target

    Returns:

    """
    return numpy.array([[dVdZ(station, target)]])
