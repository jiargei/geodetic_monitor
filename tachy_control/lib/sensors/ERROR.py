# -*- coding: utf-8 -*-


class DiMoSyError(Exception):
    """

    """
    pass


class NoSensorError(DiMoSyError):
    """

    """
    def __str__(self):
        return "Keine Sensoren gefunden, Setup wird abgebrochen"


class TargetError(Exception):

    """
    Exception to handle Target Errors
    """
    
    def __init__(self, targetName='Target', Hz=None, V=None):
        """
        :param targetName: Name of Target
        :type  targetName: str
        :param Hz        : Horizontal Angle
        :type  Hz        : float
        :param V         : Vertical Angle
        :type  V         : float
        """
        self.targetName = targetName
        self.Hz = Hz
        self.V = V
        
    def __str__(self):
        return repr(self)
    
    def __repr__(self):
        return "Error: %s not found at Hz=%.4f, V=%.4f" % (self.targetName, self.Hz, self.V)


class URLError(Exception):

    """
    Exception to handle url Errors
    """
    
    def __init__(self, url):
        """
        :param url: what kind of Sensor
        :type url: str
        """
        self.url = url
        
    def __str__(self):
        return repr(self)
    
    def __repr__(self):
        return "URL: no connection to URL %s" % self.url
    
    
class MethodError(Exception):

    """
    Exception to handle method Errors
    """
    
    def __init__(self, method, value):
        """
        :param method: what kind of Sensor
        :type method: str
        :param value: what kind of Sensor
        :type value: str
        """
        self.method = method
        self.value = value
        
    def __str__(self):
        return repr(self)
    
    def __repr__(self):
        return "Method: %s, Error: %s" % (self.method, self.value)
        

class ConnectionError(Exception):

    """
    Exception to handle communication Errors with sensors
    """
    
    def __init__(self, sensorType, sensorPosition):
        """
        :param sensorType: what kind of Sensor
        :type sensorType: str
        :param sensorPosition: which position tried to communicate with sensor
        :type sensorPosition: str
        """
        self.sensorPosition = sensorPosition
        self.sensorType = sensorType
        
    def __str__(self):
        return repr(self)
    
    def __repr__(self):
        return "%s: no connection to sensor at %s" % (self.sensorType, self.sensorPosition)
    
    
class SensorRequestError(Exception):

    """
    Exception to handle Request Errors with sensors
    """
    
    def __init__(self, sensorName, sensorError):
        """
        :param sensorName: what kind of Sensor
        :type sensorName: str
        :param sensorError: which position tried to communicate with sensor
        :type sensorError: str
        """
        self.sensorName = sensorName
        self.sensorError = sensorError
        
    def __str__(self):
        return repr(self)
    
    def __repr__(self):
        return "%s: bad Request: %s" % (self.sensorName, self.sensorError)
    
    
class BoxError(Exception):

    """
    Exception to handle Box Errors
    """
    
    def __init__(self, name, error):
        """
        :param name: what kind of Sensor
        :type name: str
        :param error: which position tried to communicate with sensor
        :type error: str
        """
        self.name = name
        self.error = error
        
    def __str__(self):
        return repr(self)
    
    def __repr__(self):
        return "%s: Error: %s" % (self.name, self.error)
    
    
class LengthMismatchError(Exception):

    """
    Exception to Lists with different length
    """
    
    def __init__(self, n1, n2):
        """
        :param n1:        length of List1
        :type n1:         int
        :param n2:        length of List2
        :type n2:         int
        """
        self.n1 = n1
        self.n2 = n2
        
    def __str__(self):
        return repr(self)
    
    def __repr__(self):
        return "Length mismatch between List1 (len=%d) and List2 (len=%d)" % (self.n1, self.n2)
