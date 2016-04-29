# -*- coding: utf-8 -*-

import numpy


def dRdX(Pi, Pk):
    return float(1 * (Pi.Y - Pk.Y) / (numpy.sqrt((Pi.X - Pk.X) ** 2 + (Pi.Y - Pk.Y) ** 2)) ** 2)
    # return float(-(Pi.Y - Pk.Y)/(Pi.X**2 - 2*Pi.X*Pk.X + Pk.X**2 + (Pi.Y - Pk.Y)**2))


def dRdY(Pi, Pk):
    return float(-1 * (Pi.X - Pk.X) / (numpy.sqrt((Pi.X - Pk.X) ** 2 + (Pi.Y - Pk.Y) ** 2)) ** 2)
    # return float( (Pi.X - Pk.X)/(Pi.Y**2 - 2*Pi.Y*Pk.Y + Pi.X**2 - 2*Pi.X*Pk.X + Pk.X**2 + Pk.Y**2) )


def dRdO(Pi, Pk):
    return 1


def dSdX(Pi, Pk):
    return float((Pi.X - Pk.X) / numpy.sqrt((Pi.X - Pk.X) ** 2 + (Pi.Y - Pk.Y) ** 2))
    # return float((1.0*Pi.X - 1.0*Pk.X)*((-Pi.X + Pk.X)**2 + (-Pi.Y + Pk.Y)**2 + (-Pi.Z + Pk.Z)**2)**(-0.5))


def dSdY(Pi, Pk):
    return float((Pi.Y - Pk.Y) / numpy.sqrt((Pi.X - Pk.X) ** 2 + (Pi.Y - Pk.Y) ** 2))
    # return float((1.0*Pi.Y - 1.0*Pk.Y)*((-Pi.X + Pk.X)**2 + (-Pi.Y + Pk.Y)**2 + (-Pi.Z + Pk.Z)**2)**(-0.5))


def dSdO(Pi, Pk):
    return 0


def design2D(Pi, Pk):
    """
    Liefert die Design-Matrix für ein einen Standpunkt und Zielpunkt.

    :type   Pi                  : Point
    :param  Pi                  : Standpunkt
    :type   Pk                  : Point
    :param  Pk                  : Zielpunkt
    :rtype: numpy.array
    :return: Desingmatrix für Zielpunkt Pk und Standpunkt Pi
    """

    "partial derivatives Distance"
#     dS_dxi = (1.0*Pi.X - 1.0*Pk.X)*((-Pi.X + Pk.X)**2 + (-Pi.Y + Pk.Y)**2 + (-Pi.Z + Pk.Z)**2)**(-0.5)
#     dS_dyi = (1.0*Pi.Y - 1.0*Pk.Y)*((-Pi.X + Pk.X)**2 + (-Pi.Y + Pk.Y)**2 + (-Pi.Z + Pk.Z)**2)**(-0.5)
#     dS_dzi = (1.0*Pi.Z - 1.0*Pk.Z)*((-Pi.X + Pk.X)**2 + (-Pi.Y + Pk.Y)**2 + (-Pi.Z + Pk.Z)**2)**(-0.5)
#     dS_doi = 0

    "partial derivatives Azimuth"
# dR_dxi = -(-Pi.Y + Pk.Y)/((-Pi.X + Pk.X)**2 + (-Pi.Y + Pk.Y)**2) # dx/dy
# dR_dyi = -(Pi.X - Pk.X)/((-Pi.X + Pk.X)**2 + (-Pi.Y + Pk.Y)**2)  #dx/dy

# dR_dxi = -(Pi.Y - Pk.Y)/((-Pi.X + Pk.X)**2 + (-Pi.Y + Pk.Y)**2) # dy/dx
# dR_dyi = -(-Pi.X + Pk.X)/((-Pi.X + Pk.X)**2 + (-Pi.Y + Pk.Y)**2) # dy/dx

#     dR_dxi = -1/((-Pi.Y + Pk.Y)*((-Pi.X + Pk.X)**2/(-Pi.Y + Pk.Y)**2 + 1))
#     dR_dyi = (-Pi.X + Pk.X)/((-Pi.Y + Pk.Y)**2*((-Pi.X + Pk.X)**2/(-Pi.Y + Pk.Y)**2 + 1))
#     dR_dzi = 0
#     dR_doi = -1

    "partial derivatives Zenith"
#     dZ_dxi = (1.0*Pi.X - 1.0*Pk.X)*(-Pi.Z + Pk.Z)*((-Pi.X + Pk.X)**2 + (-Pi.Y + Pk.Y)**2)**(-0.5)/((-Pi.Z + Pk.Z)**2 + ((-Pi.X + Pk.X)**2 + (-Pi.Y + Pk.Y)**2)**1.0)
#     dZ_dyi = (1.0*Pi.Y - 1.0*Pk.Y)*(-Pi.Z + Pk.Z)*((-Pi.X + Pk.X)**2 + (-Pi.Y + Pk.Y)**2)**(-0.5)/((-Pi.Z + Pk.Z)**2 + ((-Pi.X + Pk.X)**2 + (-Pi.Y + Pk.Y)**2)**1.0)
#     dZ_dzi = ((-Pi.X + Pk.X)**2 + (-Pi.Y + Pk.Y)**2)**0.5/((-Pi.Z + Pk.Z)**2 + ((-Pi.X + Pk.X)**2 + (-Pi.Y + Pk.Y)**2)**1.0)

#     dZ_dxi = (1.0*Pi.X - 1.0*Pk.X)*((-Pi.X + Pk.X)**2 + (-Pi.Y + Pk.Y)**2)**(-0.5)/((1 + ((-Pi.X + Pk.X)**2 + (-Pi.Y + Pk.Y)**2)**1.0/(-Pi.Z + Pk.Z)**2)*(-Pi.Z + Pk.Z))
#     dZ_dyi = (1.0*Pi.Y - 1.0*Pk.Y)*((-Pi.X + Pk.X)**2 + (-Pi.Y + Pk.Y)**2)**(-0.5)/((1 + ((-Pi.X + Pk.X)**2 + (-Pi.Y + Pk.Y)**2)**1.0/(-Pi.Z + Pk.Z)**2)*(-Pi.Z + Pk.Z))
#     dZ_dzi = ((-Pi.X + Pk.X)**2 + (-Pi.Y + Pk.Y)**2)**0.5/((1 + ((-Pi.X + Pk.X)**2 + (-Pi.Y + Pk.Y)**2)**1.0/(-Pi.Z + Pk.Z)**2)*(-Pi.Z + Pk.Z)**2)
#     dZ_doi = 0

#     return numpy.array([[float(dR_dxi), float(dR_dyi), float(dR_dzi)],
#                         [float(dZ_dxi), float(dZ_dyi), float(dZ_dzi)],
#                         [float(dS_dxi), float(dS_dyi), float(dS_dzi)]])
#     return numpy.array([[float(dR_dxi), float(dR_dyi), float(dR_dzi), float(dR_doi)],
#                         [float(dZ_dxi), float(dZ_dyi), float(dZ_dzi), float(dZ_doi)],
#                         [float(dS_dxi), float(dS_dyi), float(dS_dzi), float(dS_doi)]])

    return numpy.array([[dRdX(Pi, Pk), dRdY(Pi, Pk), dRdO(Pi, Pk)],
                        [dSdX(Pi, Pk), dSdY(Pi, Pk), dSdO(Pi, Pk)]])


def dVdZ(Pi, Pk):
    """
    Partielle Ableitung der Zenithdistanz nach der Höhe
    :param Pi:
    """
    #d = Pk.__sub__(Pi)
    Sd = Pk.dist_slope(Pi)
    Sh = Pk.dist_plane(Pi)

    return float((Sh ** 2) * (Sd ** 2) ** (-1.5) * ((Sh ** 2) / (Sd ** 2)) ** (-0.5))


def design1D(Pi, Pk):
    return numpy.array([[dVdZ(Pi, Pk)]])