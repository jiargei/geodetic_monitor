#/bin/python
# -*- coding: utf-8 -*-

import logging
from abc import ABCMeta, abstractmethod
import numpy as np

from ..point import Point
from ..adjustment.normalgleichung import normalgleichung

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Transformation(object):
    """

    """
    __metaclass__ = ABCMeta

    def __init__(self):
        self.__is_set = False

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
            lpl.append({
                "from": p,
                "to": self.transform_point(p)
            })
        return lpl

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
    def __init__(self):
        super(Helmert2DTransformation, self).__init__()
        self.__ident_from = []
        self.__ident_to = []
        self.__design_matrix = None
        self.__observation_vector = None
        self.rotation = 0.
        self.scale = 1.
        self.translation = Point(0., 0., 0.)
        self.__addition = Point()

    def set_addition(self, x, y):
        self.__addition = Point(x, y)

    def get_rotation_matrix(self):
        """

        Returns:

        """
        alpha = self.rotation * np.pi / 200.
        r = np.array([
            [np.cos(alpha), np.sin(alpha)*(-1), 0.],
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
        assert self.__is_set
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
            r: Rotation
            s: Scale

        Returns:

        """
        assert isinstance(t, Point)
        self.translation = t
        self.rotation = r
        self.scale = s
        self.__is_set = True

    def build_design(self):
        """

        Returns:

        """
        a = None
        l = None
        assert self.can_calculate()
        for i in range(len(self.__ident_from)):

            ai = self.get_ai(self.__ident_from[i])
            li = self.get_li(self.__ident_to[i])

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
        return np.array([[1, 0, p.x, -p.y],
                         [0, 1, p.y, p.x]])

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
            'rotation': self.rotation,
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
        self.__ident_from.append(p_from - self.__addition)
        self.__ident_to.append(p_to)
        return True

    def can_calculate(self):
        return len(self.__ident_from) >= 2 and len(self.__ident_from) == len(self.__ident_to)

    def calculate_parameters(self):
        """

        Returns:

        """
        assert self.can_calculate()

        P = np.eye(self.__design_matrix.shape[0])

        xx, vv, Qxx, Qll, Qlld, Qvv, s02p, HP = normalgleichung(self.__design_matrix, P, self.__observation_vector)
        a = float(xx[0])
        b = float(xx[1])
        c = float(xx[2])
        d = float(xx[3])

        self.rotation = np.mod(np.arctan2(d, c) * 200. / np.pi, 400.)
        self.scale = np.sqrt(c ** 2 + d ** 2)
        self.translation = Point(a, b, 0.)
        self.__is_set = True


class Helmert3DTransformation(Transformation):
    """

    """


class AffinTransformation(Transformation):
    """

    """