import unittest
import logging
from point import Point, MeasuredPoint, Station
from calculations.transformation import Helmert2DTransformation
from calculations.resection import Resection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TransformationTestCase(unittest.TestCase):
    """

    """

    def setUp(self):
        self.addition = Point()
        self.ident_from = []
        self.ident_to = []

        self.setup_one()

    def setup_two(self):
        """
        Punkt          Epoche     Y  [m]   X  [m]     H  [m]   Code   MS
        DP01G                     5195.093, 337187.746, 156.225         M34
        DP01L                        6.8283, 3.6133

        Profile
        P1  5187.6424, 337185.704 => 0.0, 0.0
        P2  5202.2756, 337182.444 => 14.9919, 0.0

        rotation = 13.9548 gon
        scale = 1.000002
        translation = 5187.463, 337184.074

        Returns:

        """

        self.correct_result = {
            "rotation": 13.9548,
            "scale": 1.000002,
            "translation": Point(5187.463, 337184.074),
            "points": [
                {"from": Point(7.722, 0.234)},
                {"to": Point(5195.093, 337187.746)},
            ],
        }

        self.ident_to.append(Point(5187.6424, 337185.704))
        self.ident_from.append(Point(0., 0.))
        self.ident_to.append(Point(5202.2756, 337182.444))
        self.ident_from.append(Point(14.9919, 0.))

        # self.addition = Point(5200, 337180)

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

        self.correct_result = {
            "rotation": -34.7530,
            "scale": 1.,
            "translation": Point(396.112, 217.143),
            "points": [
                {"from": Point(44.8160, 23.1717)},
                {"to": Point(428.5677, 238.1267)},
            ]
        }

        self.ident_to.append(Point(402.2956, 195.0549))
        self.ident_from.append(Point(0., 0.))
        self.ident_to.append(Point(475.0164, 239.2311))
        self.ident_from.append(Point(85.0873, 0.))

    def test_transformation(self):
        """

        Returns:

        """
        h2d = Helmert2DTransformation()
        h2d.set_addition(self.addition.x, self.addition.y)
        for i in range(len(self.ident_from)):
            h2d.add_ident_pair(self.ident_from[i], self.ident_to[i])

        h2d.calculate()
        logger.info(h2d)

        self.assertAlmostEqual(self.correct_result["scale"], h2d.get_parameters()["scale"], places=4)
        self.assertAlmostEqual(self.correct_result["rotation"], h2d.get_parameters()["rotation"], places=3)

        pl = []
        for p in self.correct_result["points"]["from"]:
            pl.append(p)

        new_points = h2d.transform(pl)

        p0 = new_points[0]
        p1 = p0["to"]
        # n = (self.points_to[0]+self.addition-p1).norm()
        # logger.info("diff: %.4f" % n)
        # self.assertTrue(n < 1e-3)


class ResectionTestCase(unittest.TestCase):
    """

    """
    def setUp(self):
        self.target_list = []
        station_name = '16-03-31.074'

        self.target_list.append(MeasuredPoint(
            27.485, 3.090, 1.021, station_name, '9001', 258.7195, 104.3508, 11.226
        ))
        self.target_list.append(MeasuredPoint(
            21.753, 7.791, 1.432, station_name, '9002', 223.0525, 104.4693, 5.081
        ))
        self.target_list.append(MeasuredPoint(
            13.382, 6.085, 1.298, station_name, '9003', 29.9477, 108.9109, 3.516
        ))
        # self.target_list.append(MeasuredPoint(
        #     None, None, 0.19, station_name, 'H1', 96.9081, 125.1134, 4.158
        # ))
        self.correct_result = Station(station_name, 16.835, 6.561, 1.788, ori=261.3388)

    def test_resection(self):
        resection = Resection(target_list=self.target_list)
        resection.calculate()

        logger.info(u"Check coordinate")
        self.assertAlmostEqual((self.correct_result-resection.station).norm(), Point().norm(), places=4)

        logger.info(u"Check orientation")
        self.assertAlmostEqual(self.correct_result.ori, resection.station.ori, places=5)
