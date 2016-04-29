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
        self.setup_two()

    def setup_two(self):
        """
        Punkt          Epoche     Y  [m]   X  [m]     H  [m]   Code   MS
        DP01G                     5195.093, 337187.746, 156.225         M34
        DP01L                        6.8283, 3.6133

        Profile
        P1  5187.6424, 337185.704 => 0.0, 0.0
        P2  5202.2756, 337182.444 => 14.9199, 0.0

        rotation = 1,7899974 rad
        scale = 1
        translation = ?

        Returns:

        """
        self.ident_from = []
        self.ident_to = []
        self.ident_from.append(Point(5187.6424, 337185.704))
        self.ident_to.append(Point(0., 0.))
        self.ident_from.append(Point(5202.2756, 337182.444))
        self.ident_to.append(Point(14.9199, 0.))

        self.points_from = [Point(5195.093, 337187.746)]
        self.points_to = [Point(7.722, 0.234)]
        self.addition = Point(5100, 337100)
        self.addition = Point()

    def setup_one(self):
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
        self.addition = Point()

    def test_transformation(self):
        """

        Returns:

        """
        h2d = Helmert2DTransformation()
        h2d.set_addition(self.addition.x, self.addition.y)
        for i in range(len(self.ident_from)):
            h2d.add_ident_pair(self.ident_from[i], self.ident_to[i])

        h2d.calculate()
        logger.info(h2d.get_parameters())
        new_points = h2d.transform(self.points_from)
        p0 = new_points[0]
        p1 = p0["to"]
        n = (self.points_to[0]+self.addition-p1).norm()
        logger.info("diff: %f" % n)
        self.assertTrue(n<1e-3)