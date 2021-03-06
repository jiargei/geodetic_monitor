from abc import abstractproperty, ABCMeta, abstractmethod
from uuid import uuid1
from datetime import datetime

import response


class Sensor(object):

    __metaclass__ = ABCMeta

    def __init__(self, connector):
        """

        :param connector:
        :return:
        """
        self.connector = connector

    @classmethod
    def get_name(cls):
        return "%s %s" % (cls.brand, cls.model)

    @abstractproperty
    def sensor_type(self):
        pass

    @abstractproperty
    def model_type(self):
        pass

    @abstractproperty
    def brand(self):
        pass

    @abstractproperty
    def model(self):
        pass

    @classmethod
    def get_sensor_type(cls):
        return response.StringResponse(string=cls.sensor_type)

    @classmethod
    def get_model_type(cls):
        return response.StringResponse(string=cls.model_type)

    @classmethod
    def get_brand(cls):
        return response.StringResponse(string=cls.brand)

    @abstractmethod
    def get_measurement(self):
        """

        :return:
        :rtype: Response
        """
        pass

    @abstractmethod
    def get_elastic_data(self, **kwargs):
        """

        Returns:

        """
        pass


def create_uid(k="UID"):
    return {k: uuid1()}


def create_date(k="CREATED"):
    return {k: datetime.now()}