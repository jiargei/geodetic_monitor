#!/bin/python
# -*- coding: utf-8 -*-

import scipy as np
import scipy.linalg
import logging

from normalgleichung import normalgleichung
from . import design

from .. point import Point, MeasuredPoint, Station
from .. measurement import TachyMeasurement
from .. adjustment.orientation import Orientation
from .. calculations.transformation import Helmert2DTransformation
from .. calculations.polar import grid_to_polar
from .. calculations import convert


logger = logging.getLogger(__name__)


class Adjustment(object):
    """

    """
    def __init__(self, station, orientation=0., target_list=[]):
        self.__is_set = False
        self.station = station
        self.target_list = target_list
        self.orientation = orientation
        self.sigma_horizontal_angle=None
        self.sigma_vertical_angle=None
        self.sigma_slope_distance=None,
        self.itsmax=100,
        self.SLLFIX=True,
        self.__a = None
        self.__l = None
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

    def add_measured_point(self, mp):
        """

        Args:
            mp: MeasuredPoint

        Returns:

        """
        assert isinstance(mp, MeasuredPoint)
        self.target_list.append(mp)

    def do_helmert_2d(self):
        """
        Bestimmung der Näherungskoordinaten mittels 2D-Helmert
        und Mittelung der Zenitdistanzen zur Höhenbestimmung.
        """
        #    ___                  _      _      _       _   _      _                     _
        #   / _ \                | |    (_)    | |     | | | |    | |                   | |
        #  / /_\ \_   _ ___  __ _| | ___ _  ___| |__   | |_| | ___| |_ __ ___   ___ _ __| |_
        #  |  _  | | | / __|/ _` | |/ _ \ |/ __| '_ \  |  _  |/ _ \ | '_ ` _ \ / _ \ '__| __|
        #  | | | | |_| \__ \ (_| | |  __/ | (__| | | | | | | |  __/ | | | | | |  __/ |  | |_
        #  \_| |_/\__,_|___/\__, |_|\___|_|\___|_| |_| \_| |_/\___|_|_| |_| |_|\___|_|   \__|
        #                    __/ |
        #                   |___/

        logger.debug("run resection")

        s02 = self.s02_apr
        n = len(self.target_list)
        sig_Hz = convert.gon2rad(self.sigma_horizontal_angle)
        sig_V = convert.gon2rad(self.sigma_vertical_angle)
        sig_Sd = self.sigma_slope_distance
        h2d = Helmert2DTransformation()

        system_global = []
        system_local = []

        for pk in self.target_list:
            ml = TachyMeasurement(pk.horizontal_angle, pk.vertical_angle, pk.slope_distance, pk.target_height)
            p_from = ml.to_grid()
            h2d.add_ident_pair(p_from, pk)

        h2d.calculate()
        self.station.x = h2d.translation.x
        self.station.y = h2d.translation.y
        self.station.z = sum(map(lambda t: t.z, self.target_list)) / len(self.target_list)

    def do_orientation(self):
        """
        Determine Orientation
        """
        logger.debug("Calculate Orientation")
        ori = Orientation()
        for ti in self.target_list:
            ori.add_angle_pair(tk=grid_to_polar(self.station, ti),
                               rk=ti.horizontal_angle)
        ori.calculate()
        logger.debug(ori.get())
        self.orientation = ori.value

    # Pi.ORI = ANGLE.corr_hz(ori["orientation"])
    # t104_113 = np.arctan((Pn[2].X - Pn[1].X)/(Pn[2].Y-Pn[1].Y))
    # D104_113 = Pn[1].dist_plane(Pn[2])
    # t104_108 = t104_113 - np.arccos( (D104_113**2 + Pn[1].SD**2 - Pn[2].SD**2)/(2*Pn[1].SD*D104_113) )
    # Pi.X = Pn[1].X + Pn[1].SD*np.sin(t104_108)
    # Pi.Y = Pn[1].Y + Pn[1].SD*np.cos(t104_108)

    def get_li(self, target):
        """

        Args:
            target:

        Returns:

        """

        tmpL = np.transpose(np.array([convert.gon2rad(target.horizontal_angle),
                                      target.get_slope_distance()
                                      ]
                                     )
                            )
        LL0 = grid_to_polar(self.station, target, self.orientation)
        tmpL0 = np.transpose(np.array([convert.gon2rad(LL0['azimut']),
                                       LL0['distancePlane']]))

        return np.array(tmpL - tmpL0)

    def do_adjustment_2D(self):
        """

        """
        #    ___                  _      _      _       _
        #   / _ \                | |    (_)    | |     | |
        #  / /_\ \_   _ ___  __ _| | ___ _  ___| |__   | |     __ _  __ _  ___
        #  |  _  | | | / __|/ _` | |/ _ \ |/ __| '_ \  | |    / _` |/ _` |/ _ \
        #  | | | | |_| \__ \ (_| | |  __/ | (__| | | | | |___| (_| | (_| |  __/
        #  \_| |_/\__,_|___/\__, |_|\___|_|\___|_| |_| \_____/\__,_|\__, |\___|
        #                    __/ |                                   __/ |
        #                   |___/                                   |___/

        logger.debug("Adjustment PLANE")
        s02 = self.s02_apr
        for its in range(self.iterations):

            """Bestimmung der Varianzmatrix"""
            sigVektor = [self.sigma_horizontal_angle ** 2, self.sigma_slope_distance ** 2]
            p = len(sigVektor)  # Anzahl der unterschiedlichen Beobachtungen
            Sll = np.mat(np.eye(len(self.target_list) * p))
            for k in range(len(self.target_list)):
                for q in range(p):
                    Sll[k * p + q, k * p + q] = sigVektor[q]

            # P = np.eye(len(Pn) * 2)
            P = scipy.linalg.inv(s02 * Sll)

            FIRST = True
            # print "%d: %s" % (its, Pi)

            a = None
            l = None

            for ti in self.target_list:
                ai = design.design2D(self.station, ti)
                li = self.get_li(target=ti)

                if a is None or l is None:
                    a = ai
                    l = li
                else:
                    a = np.vstack([a, ai])
                    l = np.vstack([l, li])

            # print "L:\n",np.transpose([L])

            x = normalgleichung(a, P, l)

            xx = x[0]
            vv = x[1]
            Qxx = x[2]
            Qll = x[3]
            Qlld = x[4]
            HP = x[7]
            # ...
            s02p = float(x[6])

            # if math.fabs(HP)<5e-4 and math.fabs(HP)>1e8:
            #     print "Verprobung nach %d Durchläufen OK"%its
            #    its = ITERATIONS
            # s02 = s02p

            # if False:
            #     print "x:\n", xx
            #     print "v:",
            #     for m in range(len(vv)):
            #         print "%10.1f [%s]" % (np.sqrt(vv[m]) * np.sqrt(s02p) * 1e3, 'cgon' if m == 2 else 'mm')
            #     print "L:\n", L
            #     print "L0:\n", L0
            #     print "l:\n", l
            #     print "A:\n", A
            #     print "P:\n", P
            #     print "\ns0:\n%e" % np.sqrt(s02p)
            #     print "\nQxx:"
            #     for m in range(len(Qxx)):
            #         print "%10.1f [%s]" % (np.sqrt(Qxx[m, m]) * np.sqrt(s02p) * 1e3, 'cgon' if m == 2 else 'mm')
            #     print "\nQlld:"
            #     for m in range(len(Qlld)):
            #         print "%10.1f [%s]" % (np.sqrt(Qlld[m, m]) * np.sqrt(s02p) * 1e3, 'cgon' if m % 2 != 0 else 'mm')
            #     print "\nQll:"
            #     for m in range(len(Qll)):
            #         print "%10.1f" % (np.sqrt(Qll[m, m] / s02p))

            self.station.x += xx[0]
            self.station.y += xx[1]
            self.orientation.value += convert.rad2gon(xx[2])
            self.orientation.value = convert.corr_hz(angle=-1 * self.orientation.value)
            self.sigma_easting = np.sqrt(Qxx[0, 0] * np.sqrt(s02p))
            self.sigma_northing = np.sqrt(Qxx[1, 1] * np.sqrt(s02p))
            self.sigma_orientation = np.sqrt(Qxx[2, 2] * np.sqrt(s02p))

    def do_adjust_1D(self):
        """
        """
    #    ___                  _      _      _       _   _ _   _ _
    #   / _ \                | |    (_)    | |     | | | (_) (_) |
    #  / /_\ \_   _ ___  __ _| | ___ _  ___| |__   | |_| | ___ | |__   ___
    #  |  _  | | | / __|/ _` | |/ _ \ |/ __| '_ \  |  _  |/ _ \| '_ \ / _ \
    #  | | | | |_| \__ \ (_| | |  __/ | (__| | | | | | | | (_) | | | |  __/
    #  \_| |_/\__,_|___/\__, |_|\___|_|\___|_| |_| \_| |_/\___/|_| |_|\___|
    #                    __/ |
    #                   |___/

        logger.debug(""".. Ausgleich Hoehe ..""")
        its = 0
        for its in range(self.iterations):

            """Bestimmung der Varianzmatrix"""
            sigVektor = [self.sigma_vertical_angle ** 2]
            p = len(sigVektor)  # Anzahl der unterschiedlichen Beobachtungen
            Sll = np.mat(np.eye(len(self.target_list) * p))
            for k in range(len(self.target_list)):
                for q in range(p):
                    Sll[k * p + q, k * p + q] = sigVektor[q]

            P = np.eye(len(self.target_list) * 2)
            P = scipy.linalg.inv(self.s02_apr * Sll)

            FIRST = True

            # Normalgleichung
            x = normalgleichung(self.__a, P, self.__l)

            xx = x[0]
            vv = x[1]
            Qxx = x[2]
            Qll = x[3]
            Qlld = x[4]
            HP = x[7]
            # ...
            s02p = float(x[6])

            self.station.z += xx[0]
            self.station.sigmaHeight = np.sqrt(Qxx[0, 0] * np.sqrt(s02p))

            # if debug_mode:
            #     print "x:\n", xx
            #     print "v:",
            #     for m in range(len(vv)):
            #         print "%10.1f [%s]" % (np.sqrt(vv[m]) * np.sqrt(s02p) * 1e3, 'cgon' if m == 2 else 'mm')
            #     print "L:\n", L
            #     print "L0:\n", L0
            #     print "l:\n", l
            #     print "A:\n", A
            #     print "P:\n", P
            #     print "\ns0:\n%e" % np.sqrt(s02p)
            #     print "\nQxx:"
            #     for m in range(len(Qxx)):
            #         print "%10.1f [%s]" % (np.sqrt(Qxx[m, m]) * np.sqrt(s02p) * 1e3, 'cgon' if m == 2 else 'mm')
            #     print "\nQlld:"
            #     for m in range(len(Qlld)):
            #         print "%10.1f [%s]" % (np.sqrt(Qlld[m, m]) * np.sqrt(s02p) * 1e3, 'cgon' if m % 2 != 0 else 'mm')


    def get_station(self):
        return self.station