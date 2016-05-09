#/bin/python
# -*- coding: utf-8 -*-

import logging
from abc import ABCMeta, abstractmethod, abstractproperty

import numpy as np

from geodetic.calculations.adjustment.normalgleichung import normalgleichung
from geodetic.calculations import polar
from ..point import Point, PointPair

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Transformation(object):
    """

    """
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        self.__is_set = True

        for k in self.get_parameter_list():
            if not k in kwargs:
                logger.debug("Trafo Key '%s' not set" % k)
                self.__is_set = False

        if not self.get_parameter_list():
            self.__is_set = False

    def get_trafo_state(self):
        return self.__is_set

    def calculate(self):
        """

        Returns:

        """
        assert self.can_calculate()
        self.build_design()
        self.calculate_parameters()
        self.__is_set = True

    def transform(self, point_list):
        """

        Args:
            point_list:

        Returns:

        """
        assert self.__is_set
        lpl = []
        for p in point_list:
            assert isinstance(p, Point)
            lpl.append(PointPair(
                p_from=p,
                p_to=self.transform_point(p),
            ))
        return lpl

    @abstractproperty
    def get_parameter_list(self):
        """

        Returns: a list containing the trafo parameter attribute keys

        """
        return []

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def get_parameters(self):
        """

        Returns:

        """

    @abstractmethod
    def transform_point(self, p):
        """

        Args:
            p:

        Returns:

        """

    @abstractmethod
    def set_parameters(self, *args):
        """

        Returns:

        """

    @abstractmethod
    def can_calculate(self):
        """

        Returns:

        """

    @abstractmethod
    def build_design(self):
        """

        Returns:

        """

    @abstractmethod
    def calculate_parameters(self):
        """

        Returns:

        """


class Helmert2DTransformation(Transformation):
    """

    """
    def __init__(self, **kwargs):
        super(Helmert2DTransformation, self).__init__(**kwargs)
        self.__ident = {
            "from": [],
            "to": [],
            "counter": 0
        }
        self.__design_matrix = None
        self.__observation_vector = None
        self.rotation = kwargs.get("rotation", 0.)
        self.scale = kwargs.get("scale", 1.)
        p = kwargs.get("translation", Point())
        assert isinstance(p, Point)
        self.translation = p
        self.__addition = Point()
        logger.debug("Set: %s" % self.get_trafo_state())

    def __str__(self):
        return "Translation: %(translation)s, Z-Rotation: %(rotation)9.5f, Scale: %(scale)10.6f" % self.get_parameters()

    def get_parameter_list(self):
        return ["translation", "rotation", "scale"]

    def set_addition(self, x, y):
        self.__addition = Point(x, y)

    def get_rotation_matrix(self):
        """

        Returns:

        """
        alpha = self.rotation
        r = np.array([
            [np.cos(alpha), -np.sin(alpha), 0.],
            [np.sin(alpha), np.cos(alpha), 0.],
            [0., 0., 1.]
        ])
        return r

    def transform_point(self, p):
        """

        Args:
            p:

        Returns:

        """
        assert self.get_trafo_state()
        t = self.translation.as_array()
        logger.debug(t)
        s = self.scale
        logger.debug(s)
        r = self.get_rotation_matrix()
        logger.debug(r)

        p1 = t + np.dot(r, p.as_array())
        p2 = Point(float(p1[0]), float(p1[1]), float(p1[2]))

        logger.debug(p2)
        return p2

    def set_parameters(self, t, r, s):
        """

        Args:
            t: Translation
            r: Rotation in gon
            s: Scale

        :type t: Point
        :type r: float
        :type s: float

        Returns:

        """
        assert isinstance(t, Point)
        self.translation = t
        self.rotation = polar.convert.gon2rad(r)
        self.scale = s
        self.__is_set = True

    def build_design(self):
        """

        Returns:

        """
        a = None
        l = None
        assert self.can_calculate()
        for i in range(self.__ident["counter"]):

            ai = self.get_ai(self.__ident["from"][i])
            li = self.get_li(self.__ident["to"][i])

            if a is None or l is None:
                a = ai
                l = li
            else:
                a = np.vstack([a, ai])
                l = np.vstack([l, li])

        self.__design_matrix = a
        self.__observation_vector = l

    @staticmethod
    def get_ai(p):
        return np.array([[1., 0., p.x, -p.y],
                         [0., 1., p.y, p.x]])

    @staticmethod
    def get_li(p):
        return np.array([
            [p.x],
            [p.y]]
        )

    def get_parameters(self):
        return {
            'translation': self.translation,
            'scale': self.scale,
            'rotation': polar.convert.rad2gon(self.rotation),
        }

    def add_ident_pair(self, p_from, p_to):
        """

        Args:
            p_from:
            p_to:

        Returns:

        """
        assert isinstance(p_from, Point)
        assert isinstance(p_to, Point)
        self.__ident["from"].append(p_from - self.__addition)
        self.__ident["to"].append(p_to)
        self.__ident["counter"] += 1
        return True

    def can_calculate(self):
        return self.has_enough_points() and self.has_same_length()

    def has_enough_points(self):
        test = self.__ident["counter"] >= 2
        if not test:
            logger.error("Not enough identical Points")
        return test

    def has_same_length(self):
        test = len(self.__ident["from"]) == len(self.__ident["to"])
        if not test:
            logger.error("Identical Point lists are not equal")
        return test

    def calculate_parameters(self):
        """

        Returns:

        """
        assert self.can_calculate()
        assert self.__design_matrix is not None

        P = np.eye(self.__design_matrix.shape[0])

        xx, vv, Qxx, Qll, Qlld, Qvv, s02p, HP = normalgleichung(self.__design_matrix, P, self.__observation_vector)
        a = float(xx[0])
        b = float(xx[1])
        c = float(xx[2])
        d = float(xx[3])

        self.rotation = -np.arctan2(d, c)
        self.scale = np.sqrt(c ** 2 + d ** 2)
        self.translation = Point(a, b, 0.)
        self.__is_set = True


class Helmert3DTransformation(Transformation):
    """

    """


class AffinTransformation(Transformation):
    """

    """