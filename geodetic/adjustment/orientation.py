import traceback
import math


class Orientation(object):
    """

    """
    def __init__(self):
        self.value = 0.
        self.sigma = 0.
        self.__t = []
        self.__r = []
        self.__is_set = False

    def is_set(self):
        return self.__is_set

    def can_calculate(self):
        if len(self.__t) >= 1:
            return True
        return False

    def add_angle_pair(self, tk, rk):
        self.__t.append(tk)
        self.__r.append(rk)

    def calculate(self):
        assert self.can_calculate()
        ori_list = map(lambda t, r: t - r, self.__t, self.__r)
        ori = sum(ori_list)/len(ori_list)
        variance_list = map(lambda o: (o - ori)**2, ori_list)
        ori_sigma = math.sqrt(sum(variance_list)/len(variance_list))

        self.value = ori
        self.sigma = ori_sigma
        self.__is_set = True

    def get(self):
        assert self.__is_set
        return {
            "orientation": self.value,
            "orientation_sigma": self.sigma
        }