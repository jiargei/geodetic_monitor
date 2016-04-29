#!/bin/python
# -*- coding: utf-8 -*-

import scipy as np
import scipy.linalg
import logging

from .. calculations import convert
    POINT, GEODETIC
from ... import VARS
from normalgleichung import normalgleichung
from .. point import Point
import design
import orientation
from .. calculations.transformation import Helmert2DTransformation

logger = logging.getLogger(__name__)


class Adjustmend(object):
    """

    """
    def __init__(self, station, target_list):
        self.__is_set = False
        self.station = station
        self.target_list = target_list

        self.sigma_horizontal_angle=None
        self.sigma_vertical_angle=None
        self.sigma_slope_distance=None,
        self.itsmax=100,
        self.SLLFIX=True,
        self.iterations=20,
        self.ASSIGN=False,
        self.PATH='',
        self.FILE='',
        self.s02_apr=1,
        self.calculate_approximation=True
    """
    **DiMoSy Berechnungen - Freie Stationierung**

    Diese Routine berechnet die Koordinaten eines Standpunktes, bezogen auf die
    eingegebene Punktliste

    ``P = np.concatenate((P,[[Xi, Yi, Zi]]))``

    und deren korrespondierenden Beobachtungen vom unbekannten Standpunkt

    ``L = np.concatenate((L,[[Sdi, ohr(Hzi), ohr(Vi)]]))``

    Bei der Eingabe das Schema beachten, die Strecken und Koordinaten in
    Einheiten [m], und die Winkelbeobachtungen in Einheiten [gon]. Eingangs
    können die gerätespezifischen Standardabweichungen festgelegt werden.

    Nach wiederholter Iteration werden die Eingangsdaten sowie die
    statistischen Angaben zum Ergebnis gezeigt. Diese beinhalten:

    **P**
       die Koordinaten der Anschlüsse

    **L**
       den Beobachtungsvektor (gemessen)

    **L0**
       den genäherten Beobachtungsvektor (gerechnet)

    **l**
       den gekürzten Beobachtungsvektor (gemessen minus gerechnet)

    **v**
       den Vektor der Verbesserungen

    **Qll**
       die Kovarianzmatrix zu den Beobachtungen

    **Qvv**
       die Kofaktormatrix zu den Verbesserungen

    **Qlld**
       die Kofaktormatrix zu den ausgeglichenen Beobachtungen

    **s02_p**
       die Gewichtseinheit a posteriori

    **sig_ll**
       die Standardabweichungen der Beobachtungen nach dem Ausgleich

    **sig_x**
       die Standardabwecihungen der Unbekannten nach dem Ausgleich

    **x**
       den Vektor der Unbekannten (Recht, Nord, Hoch, Orientierung)

    copyright 2012 by BOGENSBERGER Vermessung
    mail juergen.friedrich@bogensberger.com

    :type Pi: `Standpunkt <dimosy.TOOLS.ADJUST.html#dimosy.TOOLS.ADJUST.ADJUST.Standpunkt>`_
    :param Pi: Standpunkt
    :type Pn: tuple(`Zielunkt <dimosy.TOOLS.ADJUST.html#dimosy.TOOLS.ADJUST.ADJUST.Zielpunkt>`_)
    :param Pn: Liste von Festpunkten
    :type sigHz: float
    :param sigHz: Apriori Genauigkeit Hz-Messung [gon]
    :type sigV: float
    :param sigV: Apriori Genauigkeit V-Messung[gon]
    :type sigSd: float
    :param sigSd: Apriori Genauigkeit Streckenmessung [m]
    :type itsmax: int
    :param itsmax: Maximale Anzahl von Iterationen
    :type SLLFIX: `bool <https://docs.python.org/2/library/functions.html#bool>`_
    :param SLLFIX: kovarianz a priorie
    :type iterations: int
    :param iterations: Anzahl von Iterationen
    :type s02_apr: float
    :param s02_apr: Varianz der Gewichtseinheit apriori
    :rtype: `Standpunkt <dimosy.TOOLS.ADJUST.html#dimosy.TOOLS.ADJUST.ADJUST.Standpunkt>`_
    :return: Ausgeglichenen Koordinaten und Orientierung des Standpunktes
    """

    def do_helmert_2d(self):
        #    ___                  _      _      _       _   _      _                     _
        #   / _ \                | |    (_)    | |     | | | |    | |                   | |
        #  / /_\ \_   _ ___  __ _| | ___ _  ___| |__   | |_| | ___| |_ __ ___   ___ _ __| |_
        #  |  _  | | | / __|/ _` | |/ _ \ |/ __| '_ \  |  _  |/ _ \ | '_ ` _ \ / _ \ '__| __|
        #  | | | | |_| \__ \ (_| | |  __/ | (__| | | | | | | |  __/ | | | | | |  __/ |  | |_
        #  \_| |_/\__,_|___/\__, |_|\___|_|\___|_| |_| \_| |_/\___|_|_| |_| |_|\___|_|   \__|
        #                    __/ |
        #                   |___/

        """
        Bestimmung der Näherungskoordinaten mittels 2D-Helmert
        und Mittelung der Zenitdistanzen zur Höhenbestimmung.
        """

        logger.debug("run resection")

        s02 = self.s02_apr
        n = len(self.target_list)
        sig_Hz = convert.gon2rad(self.sigma_horizontal_angle)
        sig_V = convert.gon2rad(self.sigma_vertical_angle)
        sig_Sd = self.sigma_slope_distance

    # FILL IN
    punktVON = []
    punktNACH = []
    Z0 = []

    if debug_mode:
        print "Angabe:"
        print "Pi =      dimosy.%s" % Pi

        print "Pn = "
    for anschluss in Pn:
        if debug_mode:
            print "Pn = %s" % anschluss

    if VARS.DEBUG_MODE > 1 and debug_mode:
        print "Berechne Näherungskoordinaten:%s" % calcApproximation

    if calcApproximation:
        Pi.X = 0
        Pi.Y = 0
        Pi.Z = 0

    for Pk in Pn:

        punktNACH.append(POINT.point(X=Pk.X, Y=Pk.Y, Z=Pk.Z))
        punktVON.append(GEODETIC.polar_to_grid(P1=Pi,
                                               HZ=Pk.HZ,
                                               V=Pk.V,
                                               SD=Pk.SD))

        Z0.append(GEODETIC.polar_to_grid(P1=Pk,
                                         HZ=Pk.getHZ(),
                                         V=200 - Pk.getV(),
                                         SD=Pk.getSD()).Z)

        if VARS.DEBUG_MODE > 1 and debug_mode:
            print "Pn.append(dimosy.%s)" % Pk
            print "PunktVON : %s" % punktVON[-1]
            print "PunktNACH: %s" % punktNACH[-1]

    if calcApproximation:
        x0 = HELMERT_2D.ausgleich_helmert_2d(punktVON, punktNACH, iterations=iterations + 5, P0=Pi, debug_mode=debug_mode)
        Pi.X = x0['RW']
        Pi.Y = x0['HW']
        Pi.Z = sum(Z0) / len(Z0)

    if VARS.DEBUG_MODE > 1 and debug_mode:
        print "\nHelmert"
        print Pi

    ori = ORIENT.orient(tk=map(lambda pk: GEODETIC.grid_to_polar(Pi, pk)["azimut"], Pn),
                        Rk=map(lambda pk: pk.getHZ(), Pn))

    if VARS.DEBUG_MODE > 1 and debug_mode:
        print "\nOrientierung: %10.5f" % ANGLE.corr_hz(ori["orientation"])
        print "\nSigma:        %10.5f" % ANGLE.corr_hz(ori["sigma"])

    # Pi.ORI = ANGLE.corr_hz(ori["orientation"])

#     t104_113 = np.arctan((Pn[2].X - Pn[1].X)/(Pn[2].Y-Pn[1].Y))
#     D104_113 = Pn[1].dist_plane(Pn[2])
#     t104_108 = t104_113 - np.arccos( (D104_113**2 + Pn[1].SD**2 - Pn[2].SD**2)/(2*Pn[1].SD*D104_113) )
#
#     Pi.X = Pn[1].X + Pn[1].SD*np.sin(t104_108)
#     Pi.Y = Pn[1].Y + Pn[1].SD*np.cos(t104_108)
    if iterations > itsmax:
        iterations = itsmax
    its = 0

#    ___                  _      _      _       _
#   / _ \                | |    (_)    | |     | |
#  / /_\ \_   _ ___  __ _| | ___ _  ___| |__   | |     __ _  __ _  ___
#  |  _  | | | / __|/ _` | |/ _ \ |/ __| '_ \  | |    / _` |/ _` |/ _ \
#  | | | | |_| \__ \ (_| | |  __/ | (__| | | | | |___| (_| | (_| |  __/
#  \_| |_/\__,_|___/\__, |_|\___|_|\___|_| |_| \_____/\__,_|\__, |\___|
#                    __/ |                                   __/ |
#                   |___/                                   |___/

    if debug_mode:
        print """.. Ausgleich Lage .."""

    while its < iterations:
        # print "Iteration Nr. %02d"%its
        """Bestimmung der Varianzmatrix"""
        sigVektor = [sig_Hz ** 2, sig_Sd ** 2]
        p = len(sigVektor)  # Anzahl der unterschiedlichen Beobachtungen
        Sll = np.mat(np.eye(n * p))
        for k in range(len(Pn)):
            for q in range(p):
                Sll[k * p + q, k * p + q] = sigVektor[q]

        # P = np.eye(len(Pn) * 2)
        P = scipy.linalg.inv(s02 * Sll)

        FIRST = True
        # print "%d: %s" % (its, Pi)

        for Pj in Pn:
            # print "Punkt: %s"%Pj.NAME

            tmpA = DESIGN.design2D(Pi, Pj)
            tmpL = np.transpose(np.array([ANGLE.gon2rad(Pj.HZ), Pj.getSH()]))
            LL0 = GEODETIC.grid_to_polar(Pi, Pj, Pi.ORI)
            tmpL0 = np.transpose(np.array([ANGLE.gon2rad(LL0['azimut']), LL0['distancePlane']]))

            if FIRST:
                FIRST = False
                A = tmpA
                L = tmpL
                L0 = tmpL0
            else:
                A = np.vstack([A, tmpA])
                L = np.hstack([L, tmpL])
                L0 = np.hstack([L0, tmpL0])

        # Verkürzten Beobachtungsvektor
        l = np.transpose(np.array([L - L0]))

        # print "L:\n",np.transpose([L])

        x = normalgleichung(A, P, l)

        xx = x[0]
        vv = x[1]
        Qxx = x[2]
        Qll = x[3]
        Qlld = x[4]
        HP = x[7]
        # ...
        s02p = float(x[6])

#         if math.fabs(HP)<5e-4 and math.fabs(HP)>1e8:
#             print "Verprobung nach %d Durchläufen OK"%its
#             its = ITERATIONS
        #s02 = s02p

        if debug_mode:
            print "x:\n", xx
            print "v:",
            for m in range(len(vv)):
                print "%10.1f [%s]" % (np.sqrt(vv[m]) * np.sqrt(s02p) * 1e3, 'cgon' if m == 2 else 'mm')
            print "L:\n", L
            print "L0:\n", L0
            print "l:\n", l
            print "A:\n", A
            print "P:\n", P
            print "\ns0:\n%e" % np.sqrt(s02p)
            print "\nQxx:"
            for m in range(len(Qxx)):
                print "%10.1f [%s]" % (np.sqrt(Qxx[m, m]) * np.sqrt(s02p) * 1e3, 'cgon' if m == 2 else 'mm')
            print "\nQlld:"
            for m in range(len(Qlld)):
                print "%10.1f [%s]" % (np.sqrt(Qlld[m, m]) * np.sqrt(s02p) * 1e3, 'cgon' if m % 2 != 0 else 'mm')
            print "\nQll:"
            for m in range(len(Qll)):
                print "%10.1f" % (np.sqrt(Qll[m, m] / s02p))

        Pi.X += xx[0]
        Pi.Y += xx[1]
        Pi.ORI += ANGLE.rad2gon(xx[2])
        Pi.ORI = ANGLE.corr_hz(angle=-1 * Pi.ORI)
        its += 1

        Pi.sigmaEasting = np.sqrt(Qxx[0, 0] * np.sqrt(s02p))
        Pi.sigmaNorthing = np.sqrt(Qxx[1, 1] * np.sqrt(s02p))
        Pi.sigmaOrientation = np.sqrt(Qxx[2, 2] * np.sqrt(s02p))

#    ___                  _      _      _       _   _ _   _ _
#   / _ \                | |    (_)    | |     | | | (_) (_) |
#  / /_\ \_   _ ___  __ _| | ___ _  ___| |__   | |_| | ___ | |__   ___
#  |  _  | | | / __|/ _` | |/ _ \ |/ __| '_ \  |  _  |/ _ \| '_ \ / _ \
#  | | | | |_| \__ \ (_| | |  __/ | (__| | | | | | | | (_) | | | |  __/
#  \_| |_/\__,_|___/\__, |_|\___|_|\___|_| |_| \_| |_/\___/|_| |_|\___|
#                    __/ |
#                   |___/

    if debug_mode:
        print """.. Ausgleich Hoehe .."""

#     vv = np.zeros([len(Pn)*2,1])
    its = 0
    while its < iterations:

        its += 1

        """Bestimmung der Varianzmatrix"""
        sigVektor = [sig_V ** 2]
        p = len(sigVektor)  # Anzahl der unterschiedlichen Beobachtungen
        Sll = np.mat(np.eye(n * p))
        for k in range(len(Pn)):
            for q in range(p):
                Sll[k * p + q, k * p + q] = sigVektor[q]

        P = np.eye(len(Pn) * 2)
        P = scipy.linalg.inv(s02 * Sll)

        FIRST = True

        # Designmatrix

        for Pj in Pn:
            tmpA = DESIGN.design1D(Pi, Pj)
            tmpL = np.transpose(np.array([ANGLE.gon2rad(Pj.V)]))
            LL0 = GEODETIC.grid_to_polar(Pi, Pj, Pi.ORI)
            tmpL0 = np.transpose(np.array([ANGLE.gon2rad(LL0['zenit'])]))

            if FIRST:
                FIRST = False
                A = tmpA
                L = tmpL
                L0 = tmpL0
            else:
                A = np.vstack([A, tmpA])
                L = np.hstack([L, tmpL])
                L0 = np.hstack([L0, tmpL0])

        # Verkürzten Beobachtungsvektor
        l = np.transpose(np.array([L - L0]))

        # Normalgleichung
        x = normalgleichung(A, P, l)

        xx = x[0]
        vv = x[1]
        Qxx = x[2]
        Qll = x[3]
        Qlld = x[4]
        HP = x[7]
        # ...
        s02p = float(x[6])

        Pi.Z += xx[0]
        Pi.sigmaHeight = np.sqrt(Qxx[0, 0] * np.sqrt(s02p))

        if debug_mode:
            print "x:\n", xx
            print "v:",
            for m in range(len(vv)):
                print "%10.1f [%s]" % (np.sqrt(vv[m]) * np.sqrt(s02p) * 1e3, 'cgon' if m == 2 else 'mm')
            print "L:\n", L
            print "L0:\n", L0
            print "l:\n", l
            print "A:\n", A
            print "P:\n", P
            print "\ns0:\n%e" % np.sqrt(s02p)
            print "\nQxx:"
            for m in range(len(Qxx)):
                print "%10.1f [%s]" % (np.sqrt(Qxx[m, m]) * np.sqrt(s02p) * 1e3, 'cgon' if m == 2 else 'mm')
            print "\nQlld:"
            for m in range(len(Qlld)):
                print "%10.1f [%s]" % (np.sqrt(Qlld[m, m]) * np.sqrt(s02p) * 1e3, 'cgon' if m % 2 != 0 else 'mm')

    if debug_mode:
        print ".. Ausgleich abgeschlossen .."
        print "\nPi   =   dimosy.%s\n" % Pi

    return Pi