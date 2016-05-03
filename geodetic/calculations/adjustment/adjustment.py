#!/bin/python
# -*- coding: utf-8 -*-

import logging
from abc import ABCMeta, abstractmethod, abstractproperty

import scipy

from geodetic.calculations import convert
from geodetic.calculations.polar import grid_to_polar
from geodetic.calculations.transformation import Helmert2DTransformation
from geodetic.measurement import TachyMeasurement
from geodetic.point import MeasuredPoint, Station
from normalgleichung import normalgleichung
from . import design
from .. adjustment.orientation import Orientation

logger = logging.getLogger(__name__)


class Adjustment(object):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        """

        Args:
            s02_apr:

        Returns:

        """
        self.s02_apr = kwargs.get("s02_apr")
        self.s02 = self.s02_apr
        self.s02_post = 1.
        self.use_s02_post = True
        self.station = kwargs.get("station", Station())
        self.target_list = []
        self.iterations = kwargs.get("iterations", 20)
        self.__a = None
        self.__l = None

    def clear_a(self):
        self.__a = None

    def add_target(self, t):
        assert isinstance(t, self.get_target_class())
        self.target_list.append(t)

    def calculate_post(self):
        pass

    def calculate(self):
        """

        Returns:

        """
        assert self.can_calculate()
        
        for iteration in range(self.iterations):
            self.clear_a()
            for ti in self.target_list:
                ai = self.get_ai(ti)
                li = self.get_li(ti)
                self.add_equation(ai, li)
    
            x = normalgleichung(self.__a, self.get_p(), self.__l)
            xx = x[0]
            vv = x[1]
            Qxx = x[2]
            Qll = x[3]
            Qlld = x[4]
            HP = x[7]

            self.s02_post = float(x[6])
            if self.use_s02_post:
                self.s02 = self.s02_post

            self.add_xx(xx)
            if not self.is_relevant(xx):
                continue

        self.calculate_post()

    def add_equation(self, ai, li):
        """

        Args:
            ai:
            li:

        Returns:

        """
        a = self.__a
        l = self.__l

        if a is None or l is None:
            a = ai
            l = li
        else:
            a = scipy.vstack([a, ai])
            l = scipy.vstack([l, li])

        self.__a = a
        self.__l = l

    @abstractproperty
    def get_target_class(self):
        pass

    @abstractmethod
    def is_relevant(self, xx):
        pass

    @abstractmethod
    def add_xx(self, xx):
        pass

    @abstractmethod
    def get_p(self):
        pass

    @abstractmethod
    def get_li(self, t):
        pass

    @abstractmethod
    def get_ai(self, t):
        pass

    @abstractmethod
    def can_calculate(self):
        pass

    @abstractmethod
    def get_approximation(self):
        pass


class Adjustment1D(Adjustment):
    """
    Adjustment for height
    """
    def __init__(self, **kwargs):
        super(Adjustment1D, self).__init__(**kwargs)
        self.sigma_vertical_angle = kwargs.get("sigma_vertical_angle", 10e-4)

    def get_target_class(self):
        return MeasuredPoint

    def add_xx(self, xx):
        self.station.z += xx[0]

    def get_p(self):
        sigma_vector = [self.sigma_vertical_angle ** 2]
        p = len(sigma_vector)  # Anzahl der unterschiedlichen Beobachtungen
        sll = scipy.mat(scipy.eye(len(self.target_list) * p))
        for k in range(len(self.target_list)):
            for q in range(p):
                sll[k * p + q, k * p + q] = sigma_vector[q]

        # return scipy.eye(len(Pn) * 2)
        return scipy.linalg.inv(self.s02 * sll)

    def get_li(self, t):
        tli = scipy.transpose(scipy.array([convert.gon2rad(t.vertical_angle)]))
        ll0 = grid_to_polar(self.station, t)
        tl0 = scipy.transpose(scipy.array([convert.gon2rad(ll0['zenit'])]))
        return scipy.transpose(scipy.array([tli - tl0]))

    def is_relevant(self, xx):
        return float(xx[0] > 5e-4)

    def get_ai(self, t):
        return design.design_1d(self.station, target=t)

    def can_calculate(self):
        return len(self.target_list) >= 1

    def get_approximation(self):
        self.station.z = sum(map(lambda t: t.z, self.target_list)) / len(self.target_list)


class Adjustment2D(Adjustment):
    """
    Adjustment for easting and northing
    """

    def __init__(self, **kwargs):
        super(Adjustment2D, self).__init__(**kwargs)
        self.sigma_vertical_angle = kwargs.get("sigma_vertical_angle", 10e-4)
        self.sigma_horizontal_angle = kwargs.get("sigma_horizontal_angle", 10e-4)
        self.sigma_slope_distance = kwargs.get("sigma_slope_distance", 3e-3)
        self.orientation = Orientation()

    def get_target_class(self):
        return MeasuredPoint

    def add_xx(self, xx):
        self.station.x += xx[0]
        self.station.y += xx[1]
        self.orientation.value += convert.rad2gon(xx[2])
        self.orientation.value = convert.corr_hz(angle=-1 * self.orientation.value)

    def get_p(self):
        return scipy.eye(len(self.target_list))

    def get_li(self, t):
        tli = scipy.transpose(scipy.array([convert.gon2rad(t.horizontal_angle), t.get_slope_distance()]))
        ll0 = grid_to_polar(self.station, t, self.orientation)
        tl0 = scipy.transpose(scipy.array([convert.gon2rad(ll0['azimut']), ll0['distancePlane']]))
        return scipy.transpose(scipy.array([tli - tl0]))

    def get_ai(self, t):
        return design.design_2d(self.station, t)

    def can_calculate(self):
        return len(self.target_list) >= 2

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

    def calculate_post(self):
        ori_old = self.orientation.value
        self.do_orientation()
        ori_new = self.orientation.value
        d_ori = ori_new - ori_old
        logger.debug("Orientation Adjustment: %.4f" % ori_old)
        logger.debug("Orientation Classic: %.4f" % ori_new)

    def get_approximation(self):
        h2d = Helmert2DTransformation()

        for tig in self.target_list:
            ml = TachyMeasurement(tig.horizontal_angle, tig.vertical_angle, tig.slope_distance, tig.target_height)
            til = ml.to_grid()
            h2d.add_ident_pair(til, tig)

        h2d.calculate()
        self.station.x = h2d.translation.x
        self.station.y = h2d.translation.y
        self.station.z = sum(map(lambda t: t.z, self.target_list)) / len(self.target_list)

        self.do_orientation()

    def is_relevant(self, xx):
        return float(xx[0]) >= 5e-4 and \
               float(xx[1]) >= 5e-4


class AdjustmentOld(object):
    """

    """
    def __init__(self, station, orientation=0., target_list=[]):
        self.__is_set = False
        self.station = station
        self.target_list = target_list
        self.orientation = orientation
        self.sigma_horizontal_angle = 10e-4
        self.sigma_vertical_angle = 10e-4
        self.sigma_slope_distance = 3e-3
        self.itsmax = 100
        self.SLLFIX = True
        self.__a = None
        self.__l = None
        self.iterations = 20
        self.ASSIGN = False
        self.PATH = ''
        self.FILE = ''
        self.s02_apr = 1
        self.calculate_approximation = True
    """
    **DiMoSy Berechnungen - Freie Stationierung**

    Diese Routine berechnet die Koordinaten eines Standpunktes, bezogen auf die
    eingegebene Punktliste

    ``P = scipy.concatenate((P,[[Xi, Yi, Zi]]))``

    und deren korrespondierenden Beobachtungen vom unbekannten Standpunkt

    ``L = scipy.concatenate((L,[[Sdi, ohr(Hzi), ohr(Vi)]]))``

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
        # self.station.z = sum(map(lambda t: t.z, self.target_list)) / len(self.target_list)

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
        # t104_113 = scipy.arctan((Pn[2].X - Pn[1].X)/(Pn[2].Y-Pn[1].Y))
        # D104_113 = Pn[1].dist_plane(Pn[2])
        # t104_108 = t104_113 - scipy.arccos( (D104_113**2 + Pn[1].SD**2 - Pn[2].SD**2)/(2*Pn[1].SD*D104_113) )
        # Pi.X = Pn[1].X + Pn[1].SD*scipy.sin(t104_108)
        # Pi.Y = Pn[1].Y + Pn[1].SD*scipy.cos(t104_108)

    def get_li(self, target):
        """

        Args:
            target:

        Returns:

        """

        tmpL = scipy.transpose(scipy.array([convert.gon2rad(target.horizontal_angle),
                                      target.get_slope_distance()
                                      ]
                                     )
                            )
        LL0 = grid_to_polar(self.station, target, self.orientation)
        tmpL0 = scipy.transpose(scipy.array([convert.gon2rad(LL0['azimut']),
                                       LL0['distancePlane']]))

        return scipy.array(tmpL - tmpL0)

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
            Sll = scipy.mat(scipy.eye(len(self.target_list) * p))
            for k in range(len(self.target_list)):
                for q in range(p):
                    Sll[k * p + q, k * p + q] = sigVektor[q]

            # P = scipy.eye(len(Pn) * 2)
            P = scipy.linalg.inv(s02 * Sll)

            FIRST = True
            # print "%d: %s" % (its, Pi)

            a = None
            l = None

            for ti in self.target_list:
                ai = design.design_2d(self.station, ti)
                li = self.get_li(target=ti)

                if a is None or l is None:
                    a = ai
                    l = li
                else:
                    a = scipy.vstack([a, ai])
                    l = scipy.vstack([l, li])

            # print "L:\n",scipy.transpose([L])

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
            #         print "%10.1f [%s]" % (scipy.sqrt(vv[m]) * scipy.sqrt(s02p) * 1e3, 'cgon' if m == 2 else 'mm')
            #     print "L:\n", L
            #     print "L0:\n", L0
            #     print "l:\n", l
            #     print "A:\n", A
            #     print "P:\n", P
            #     print "\ns0:\n%e" % scipy.sqrt(s02p)
            #     print "\nQxx:"
            #     for m in range(len(Qxx)):
            #         print "%10.1f [%s]" % (scipy.sqrt(Qxx[m, m]) * scipy.sqrt(s02p) * 1e3, 'cgon' if m == 2 else 'mm')
            #     print "\nQlld:"
            #     for m in range(len(Qlld)):
            #         print "%10.1f [%s]" % (scipy.sqrt(Qlld[m, m]) * scipy.sqrt(s02p) * 1e3, 'cgon' if m % 2 != 0 else 'mm')
            #     print "\nQll:"
            #     for m in range(len(Qll)):
            #         print "%10.1f" % (scipy.sqrt(Qll[m, m] / s02p))

            self.station.x += xx[0]
            self.station.y += xx[1]
            self.orientation.value += convert.rad2gon(xx[2])
            self.orientation.value = convert.corr_hz(angle=-1 * self.orientation.value)
            self.sigma_easting = scipy.sqrt(Qxx[0, 0] * scipy.sqrt(s02p))
            self.sigma_northing = scipy.sqrt(Qxx[1, 1] * scipy.sqrt(s02p))
            self.sigma_orientation = scipy.sqrt(Qxx[2, 2] * scipy.sqrt(s02p))

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
            Sll = scipy.mat(scipy.eye(len(self.target_list) * p))
            for k in range(len(self.target_list)):
                for q in range(p):
                    Sll[k * p + q, k * p + q] = sigVektor[q]

            P = scipy.eye(len(self.target_list) * 2)
            P = scipy.linalg.inv(self.s02_apr * Sll)

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
            self.station.sigmaHeight = scipy.sqrt(Qxx[0, 0] * scipy.sqrt(s02p))

            # if debug_mode:
            #     print "x:\n", xx
            #     print "v:",
            #     for m in range(len(vv)):
            #         print "%10.1f [%s]" % (scipy.sqrt(vv[m]) * scipy.sqrt(s02p) * 1e3, 'cgon' if m == 2 else 'mm')
            #     print "L:\n", L
            #     print "L0:\n", L0
            #     print "l:\n", l
            #     print "A:\n", A
            #     print "P:\n", P
            #     print "\ns0:\n%e" % scipy.sqrt(s02p)
            #     print "\nQxx:"
            #     for m in range(len(Qxx)):
            #         print "%10.1f [%s]" % (scipy.sqrt(Qxx[m, m]) * scipy.sqrt(s02p) * 1e3, 'cgon' if m == 2 else 'mm')
            #     print "\nQlld:"
            #     for m in range(len(Qlld)):
            #         print "%10.1f [%s]" % (scipy.sqrt(Qlld[m, m]) * scipy.sqrt(s02p) * 1e3, 'cgon' if m % 2 != 0 else 'mm')


    def get_station(self):
        return self.station