import unittest
import logging
from point import Point
from calculations.transformation import Helmert2DTransformation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TransformationTestCase(unittest.TestCase):
    """

    """
    def setUp(self):
        """

        P1G: X=402.2956  Y=195.0549  Z=0
        P1L: X=  0.0000  Y=  0.0000  Z=0
        P2G: X=475.0164  Y=239.2311  Z=0
        P2L: X= 85.0873  Y=  0.0000  Z=0
        PNG: X=428.5677  Y=238.1267  Z=0
        PNL: X= 44.8160  Y= 23.1717  Z=0

        Translation: X = 53.0114 Y = 38.0595 Z = 0.0000
        Rotation: 0.5458827475 rad
        Returns:

        """
        self.ident_from = []
        self.ident_to = []
        self.ident_from.append(Point(402.2956, 195.0549))
        self.ident_to.append(Point(0., 0.))
        self.ident_from.append(Point(475.0164, 239.2311))
        self.ident_to.append(Point(85.0873, 0.))

        self.points_from = [Point(428.5677, 238.1267)]
        self.points_to = [Point(44.8160, 23.1717)]

    def test_transformation(self):
        """

        Returns:

        """
        h2d = Helmert2DTransformation()
        for i in range(len(self.ident_from)):
            h2d.add_ident_pair(self.ident_from[i], self.ident_to[i])

        h2d.calculate()
        logger.debug(h2d.get_parameters())
        new_points = h2d.transform(self.points_from)
        p0 = new_points[0]
        p1 = p0["to"]
        self.assertTrue((self.points_to[0]-p1).norm()<1e-3)
