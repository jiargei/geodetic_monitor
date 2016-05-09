import unittest
import logging
from point import Point, MeasuredPoint, Station, PointPair
from calculations.transformation import Helmert2DTransformation
from calculations.resection import Resection
from calculations.adjustment.adjustment import Helmert2DAdjustment
from calculations import convert

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TransformationTestCase(unittest.TestCase):
    """

    """

    def setUp(self):
        self.addition = Point()
        self.identical = []

        self.setup_one()

    def setup_one(self):
        """

        S1-1G: X=402.2956  Y=195.0549  Z=0
        S1-1L: X=  0.0000  Y=  0.0000  Z=0
        S1-2G: X=475.0164  Y=239.2311  Z=0
        S1-2L: X= 85.0873  Y=  0.0000  Z=0
        S1-NG: X=428.5677  Y=238.1267  Z=0
        S1-NL: X= 44.8160  Y= 23.1717  Z=0

        Translation: X = 53.0114 Y = 38.0595 Z = 0.0000
        Rotation: 0.5458827475 rad
        Returns:

        """

        self.correct_result = {
            "description": "Setup ONE",
            "transformation": Helmert2DTransformation(
                rotation=convert.gon2rad(-34.7530),
                scale=1.,
                translation=Point(396.112, 217.143)
            ),
            "points": [
                PointPair(Point(44.8160, 23.1717), Point(428.5677, 238.1267)),
            ]}
        self.identical.append(PointPair(Point(0., 0.), Point(402.2956, 195.0549)))
        self.identical.append(PointPair(Point(85.0873, 0.), Point(475.0164, 239.2311)))

    def setup_two(self):
        """
        Punkt          Epoche     Y  [m]   X  [m]     H  [m]   Code   MS
        DP01G                     5195.093, 337187.746, 156.225         M34
        DP01L                        6.8283, 3.6133

        Profile
        S2-1G: X=5187.6424 Y=337185.7040 Z=0
        S2-1L: X=   0.0000 Y=     0.0000 Z=0
        S2-2G: X=5202.2756 Y=337182.4440 Z=0
        S2-2L: X=  14.9919 Y=     0.0000 Z=0
        S2-NL: X=   7.7220 Y=     0.2340 Z=0
        S2-NG: X=5195.0930 Y=337187.7460 Z=0

        rotation = 13.9548 gon
        scale = 1.000002
        translation = 5187.463, 337184.074

        Returns:

        """

        self.correct_result = {
            "description": "Setup TWO",
            "transformation": Helmert2DTransformation(
                rotation=convert.gon2rad(13.9548),
                scale=1.000002,
                translation=Point(5187.463, 337184.074)
            ),
            "points": [
                PointPair(Point(7.722, 0.234), Point(5195.093, 337187.746)),
            ],
        }

        self.identical.append(PointPair(Point(0., 0.), Point(5187.6424, 337185.704)))
        self.identical.append(PointPair(Point(14.9919, 0.), Point(5202.2756, 337182.444)))
        # self.addition = Point(5200, 337180)

    def test_transformation(self):
        """

        Returns:

        """
        logger.info("Running configuration: '%s'" % self.correct_result["description"])
        h2d = Helmert2DAdjustment()
        for ip in self.identical:
            h2d.add_target(ip)
        h2d.calculate()

        h2d = Helmert2DTransformation(
            # translation=h2d.station,
            # rotation=h2d.rotation,
            # scale=h2d.scale
        )
        h2d.set_addition(self.addition.x, self.addition.y)
        for i in range(len(self.identical)):
            h2d.add_ident_pair(self.identical[i].get_from(), self.identical[i].get_to())

        h2d.calculate()

        logger.info("corr: %s" % self.correct_result["transformation"])
        logger.info("calc: %s" % h2d)

        new_point = h2d.transform([(self.correct_result["points"][0]).get_from()])[0]
        p_diff = new_point.get_to() - self.correct_result["points"][0].get_to()
        logger.info("Result for transformed Point:")
        logger.info("corr: %s" % self.correct_result["points"][0].get_to())
        logger.info("calc: %s" % new_point.get_to())
        logger.info("diff: %s" % p_diff)
        self.assertAlmostEqual(p_diff.norm(), Point().norm(), places=3)

        self.assertAlmostEqual(self.correct_result["transformation"].scale,
                               h2d.scale, places=4)
        self.assertAlmostEqual(self.correct_result["transformation"].rotation,
                               h2d.rotation, places=3)


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
        station_diff = resection.station - self.correct_result
        self.assertAlmostEqual(station_diff.norm(), Point().norm(), places=4)

        logger.info(u"Check orientation")
        self.assertAlmostEqual(self.correct_result.ori, resection.station.ori, places=5)
