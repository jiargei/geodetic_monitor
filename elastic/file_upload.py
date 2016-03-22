from elasticsearch import Elasticsearch
import random
import logging
import datetime

from elastic.common import utils
from elastic.common import constants


class Measurement(object):
    """
    just a test class to handle tachy measurement data
    """
    def __init__(self, *args, **kwargs):
        self.id = kwargs.get("id")
        self.created = kwargs.get("created")
        self.position = kwargs.get("position")
        self.target = kwargs.get("target")
        self.face = kwargs.get("face")
        self.easting = kwargs.get("easting")
        self.northing = kwargs.get("northing")
        self.height = kwargs.get("height")

    def __str__(self):
        return "From Position '%(position)s' to Target '%(target)s' in face %(face)d: e=%(easting)7.3f, n=%(northing)7.3f, h=%(height)7.3f" % self.__dict__


def run(its=10):
    """
    creates random tachy measurement data for elasticsearch server

    :param its: how many iterations to create pairs of positions and targets
    :return:
    """
    es = Elasticsearch()

    logging.basicConfig(level=logging.INFO)
    logging.debug("init positions")

    position_dict = {
        "positions": [
            {
                "name": "pos11",
                "easting": 0.105,
                "northing": 4.195,
                "height": 10.581,
            },
            {
                "name": "pos22",
                "easting": 85.581,
                "northing": 12.802,
                "height": 13.774,
            }
        ]
    }

    logging.debug("init targets")

    target_dict = {
        "targets": [
            {
                "name": "fp01",
                "easting": 77.185,
                "northing": 1.494,
                "height": 19.185,
            },
            {
                "name": "fp02",
                "easting": 58.195,
                "northing": 4.419,
                "height": 9.915,
            },
            {
                "name": "fp03",
                "easting": 1.069,
                "northing": 66.191,
                "height": 12.811,
            },
            {
                "name": "dp01",
                "easting": 45.195,
                "northing": 11.184,
                "height": 14.105,
            },
            {
                "name": "dp02",
                "easting": 51.918,
                "northing": 11.158,
                "height": 11.195,
            },
            {
                "name": "dp03",
                "easting": 59.171,
                "northing": 11.195,
                "height": 11.101,
            },
            {
                "name": "dp04",
                "easting": 23.199,
                "northing": 55.191,
                "height": 7.154,
            },
            {
                "name": "dp05",
                "easting": 61.118,
                "northing": 97.195,
                "height": 9.981,
            }
            ]
    }


    # you can specify to sniff on startup to inspect the cluster and load
    # balance across all nodes
    es = Elasticsearch()
    # es.indices.create(index="dimosy", ignore=400, body=constants.DIMOSY_TACHY_MEASUREMENT_MAP)
    es.indices.create(index="dimosy", ignore=400, body=constants.DIMOSY_TACHY_TEST_MAP)

    logging.debug("Create measurements")
    k = 0

    for p in position_dict["positions"]:
        for i in range(its):
            for f in [1, 2]:
                for t in target_dict["targets"]:
                    k += 1
                    m = Measurement(position=p["name"],
                                    target=t["name"],
                                    face=f,
                                    created=datetime.datetime.now(),
                                    id=k,
                                    easting=t["easting"] + random.random(),
                                    northing=t["northing"] + random.random(),
                                    height=t["height"] + random.random())
                    # logging.debug(m)
                    es.index(index='dimosy', doc_type='tachy_test', body=m.__dict__, id=m.id)
