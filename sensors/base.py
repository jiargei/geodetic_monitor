class Sensor(object):
    brand = None
    model = None
    sensor_type = None

    def get_name(self):
        return "%s %s" % (self.brand, self.model)
