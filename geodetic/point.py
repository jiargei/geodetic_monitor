# -*- coding: utf-8 -*-

import math

#  ______            _    _   _    _
#  | ___ \          | |  | | | |  | |
#  | |_/ /   _ _ __ | | _| |_| | _| | __ _ ___ ___  ___
#  |  __/ | | | '_ \| |/ / __| |/ / |/ _` / __/ __|/ _ \
#  | |  | |_| | | | |   <| |_|   <| | (_| \__ \__ \  __/
#  \_|   \__,_|_| |_|_|\_\\__|_|\_\_|\__,_|___/___/\___|
#
#


class Point2D(object):
    """

    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Point2D [x: %f, y: %f]" % (self.x, self.y)

    def __str__(self):
        return self.__repr__()


class Point():

    """Point class with public x, y and z attributes """
 
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def set_coordinate(self, coordinate):
        """

        :param coordinate:
        :return:
        """
        self.x = coordinate['x']
        self.y = coordinate['y']
        self.z = coordinate['z']


    def dist_slope(self, p):
        """return the Euclidian distance between self and p"""
        dx = self.x - p.x
        dy = self.y - p.y
        dz = self.z - p.z
        return math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    
    def dist_plane(self, p):
        """returns the planar Euclidian distance between self and p"""
        dx = self.x - p.x
        dy = self.y - p.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def dist_height(self, p):
        """
        returns the height difference between self and p

        :return: height difference between this and another point
        :rtype: double

        """
        return self.z - p.z
 
    def reset(self):
        """
        Sets this point to origin

        :return:
        """
        self.x = 0
        self.y = 0
        self.z = 0
        
    def shift(self, p):
        """
        Shifts a Point about p

        :param p:
        :type p: Point
        :return:
        """
        self.x += p.x
        self.y += p.y
        self.z += p.z
        
    def dot(self, p):
        """
        Dot product between two Points
        :rtype: float
        :return: dot product between this and p Point
        """
        return self.x * p.x + self.y * p.y + self.z * p.z
        
    def norm2D(self):
        """
        Norm from 2D Point to origin (0,0) 
        """
        return self.dist_plane(Point())

    def norm(self):
        """
        Norm from 3D Point to origin (0,0) 
        """
        return self.dist_slope(Point())
    
    def __add__(self, p):
        """return a new Point found by adding self and p. This method is
        called by e.g. p+q for Points p and q"""
        return Point(self.x + p.x, self.y + p.y, self.z + p.z)
    
    def __sub__(self, p):
        """return a new Point found by subtracting self and p. This method is
        called by e.g. p-q for Points p and q"""
        return Point(self.x - p.x, self.y - p.y, self.z - p.z)
 
    def __repr__(self):
        """return a string representation of this Point. This method is
        called by the repr() function, and
        also the str() function. It should produce a string that, when
        evaluated, returns a Point with the
        same data."""
        return 'Point(x=%12.3f,y=%12.3f,z=%12.3f)' % (self.x, self.y, self.z)
    
    def to_dict(self):
        return {'EASTING': self.x,
                'NORTHING': self.y,
                'HEIGHT': self.z}
        
    def dict_to_class(self, point_dict):
        self.x = point_dict['x']
        self.y = point_dict['y']
        self.z = point_dict['z']
        
    def class_to_list(self):
        """

        :return:
        """
        return [self.x, self.y, self.z]
    
    def class_to_dict(self):
        """

        :return:
        :rtype: dict
        """
        return {'x': self.x,
                'y': self.y,
                'z': self.z}
