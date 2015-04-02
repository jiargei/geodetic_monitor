# -*- coding: utf-8 -*-

import io
import serial


#from .. import DATABASE
# import inspect, traceback #For debug - line number


class Con(object):

    # class SensorError(Exception):
    #
    #     def __init__(self, value):
    #         self.value = value
    #
    #     def __str__(self):
    #         return repr(self.value)

    def __init__(self,
                 BAUDRATE=19200,
                 STOPBITS=1,
                 BYTESIZE=8,
                 PATH='/dev/ttyUSB0',
                 PARITY='N',
                 RTSCTS=False,
                 TIMEOUT=15.0,
                 XONXOFF=False,
                 DSRDTR=False,
                 WRITE_TIMEOUT=5.0,
                 WAIT_MEASURE=2,
                 ADDRESS='FF',
                 end_symbol="\r\n"):

        self.__BAUDRATE = BAUDRATE if BAUDRATE else 19200
        self.__STOPBITS = STOPBITS if STOPBITS else 1
        self.__BYTESIZE = BYTESIZE if BYTESIZE else 8
        self.__PATH = PATH if PATH else '/dev/ttyUSB0'
        self.__PARITY = PARITY if PARITY else 'E'
        self.__ADDRESS = ADDRESS if ADDRESS else 'FF'
        self.__RTSCTS = RTSCTS if RTSCTS else False
        self.__TIMEOUT = TIMEOUT if TIMEOUT else 5.0
        self.__XONXOFF = XONXOFF if XONXOFF else False
        self.__WRITE_TIMEOUT = WRITE_TIMEOUT if WRITE_TIMEOUT else 5.0
        self.__WAIT_MEASURE = WAIT_MEASURE if WAIT_MEASURE else 2.0
        self.__ERRORCODE = ''
        self.__RETURNCODE = ''
        self.__OUT = ''
        self.__NAME = None
        self.__SERIAL_NUMBER = None
        self.__SIGNAL_DELAY = 10
        self.sio = None
        self.end_symbol = end_symbol

    def get_address(self):
        return self.__ADDRESS

    def set_address(self, value):
        self.__ADDRESS = value

    def del_address(self):
        del self.__ADDRESS

    def __del__(self):
        self.SERIAL.close()

    def get_returncode(self):
        return self.__RETURNCODE

    def set_returncode(self, value):
        self.__RETURNCODE = value

    def del_returncode(self):
        del self.__RETURNCODE

    def get_signal_delay(self):
        return self.__SIGNAL_DELAY

    def set_signal_delay(self, value):
        self.__SIGNAL_DELAY = value

    def del_signal_delay(self):
        del self.__SIGNAL_DELAY

    def get_baudrate(self):
        return self.__BAUDRATE

    def get_stopbits(self):
        return self.__STOPBITS

    def get_bytesize(self):
        return self.__BYTESIZE

    def get_path(self):
        return self.__PATH

    def get_parity(self):
        return self.__PARITY

    def get_rtscts(self):
        return self.__RTSCTS

    def get_timeout(self):
        return self.__TIMEOUT

    def get_xonxoff(self):
        return self.__XONXOFF

    def get_wait_measure(self):
        return self.__WAIT_MEASURE

    def get_errorcode(self):
        return self.__ERRORCODE

    def get_out(self):
        return self.__OUT

    def get_name(self):
        return self.__NAME

    def get_serial_number(self):
        return self.__SERIAL_NUMBER

    def set_baudrate(self, value):
        self.__BAUDRATE = value

    def set_stopbits(self, value):
        self.__STOPBITS = value

    def set_bytesize(self, value):
        self.__BYTESIZE = value

    def set_path(self, value):
        self.__PATH = value

    def set_parity(self, value):
        self.__PARITY = value

    def set_rtscts(self, value):
        self.__RTSCTS = value

    def set_timeout(self, value):
        self.__TIMEOUT = value

    def set_xonxoff(self, value):
        self.__XONXOFF = value

    def set_wait_measure(self, value):
        self.__WAIT_MEASURE = value

    def set_errorcode(self, value):
        self.__ERRORCODE = value

    def set_out(self, value):
        self.__OUT = value

    def set_name(self, value):
        self.__NAME = value

    def set_serial_number(self, value):
        self.__SERIAL_NUMBER = value

    def del_baudrate(self):
        del self.__BAUDRATE

    def del_stopbits(self):
        del self.__STOPBITS

    def del_bytesize(self):
        del self.__BYTESIZE

    def del_path(self):
        del self.__PATH

    def del_parity(self):
        del self.__PARITY

    def del_rtscts(self):
        del self.__RTSCTS

    def del_timeout(self):
        del self.__TIMEOUT

    def del_xonxoff(self):
        del self.__XONXOFF

    def del_wait_measure(self):
        del self.__WAIT_MEASURE

    def del_errorcode(self):
        del self.__ERRORCODE

    def del_out(self):
        del self.__OUT

    def del_name(self):
        del self.__NAME

    def del_serial_number(self):
        del self.__SERIAL_NUMBER

    def load_serial_number(self):
        self.SERIAL_NUMBER = None
        return self.SERIAL_NUMBER

    def load_name(self):
        self.SNR = None
        return self.NAME

    def check_open(self):
        if not self.SERIAL.isOpen():
            self.SERIAL.open()

    def connect(self):
        try:
            self.SERIAL = serial.Serial(port=self.PATH,
                                        baudrate=self.BAUDRATE,
                                        stopbits=self.STOPBITS,
                                        bytesize=self.BYTESIZE,
                                        rtscts=self.RTSCTS,
                                        timeout=self.TIMEOUT,
                                        xonxoff=self.XONXOFF,
                                        parity=self.PARITY,
                                        writeTimeout=self.__WRITE_TIMEOUT)
        # self.SERIAL.opcd Dok    dim    en()
        # self.SERIAL.isOpen()

            if not self.SERIAL.isOpen():
                self.SERIAL.open()

            # if self.SERIAL.isOpen():
            #     return True
            # else:
            #     self.SERIAL.open()
            #     return False
            self.sio = io.TextIOWrapper(buffer=io.BufferedRWPair(self.SERIAL,
                                                                 self.SERIAL),
                                        line_buffering=True)

        finally:
            pass


    def disconnect(self):
        self.SERIAL.close()

    def reconnect(self):
        self.SERIAL.flush()
        self.SERIAL.flushInput()
        self.SERIAL.flushOutput()
        self.disconnect()
        self.connect()

    def write_line(self, line_string):
        self.check_open()
        # self.sio.write(unicode(line_string))
        self.SERIAL.write(line_string)

    def read_line(self):
        # self.sio.flush()
        # return self.sio.readline()
        return self.SERIAL.readline()

    BAUDRATE = property(get_baudrate, set_baudrate, del_baudrate, "BAUDRATE's docstring")
    STOPBITS = property(get_stopbits, set_stopbits, del_stopbits, "STOPBITS's docstring")
    BYTESIZE = property(get_bytesize, set_bytesize, del_bytesize, "BYTESIZE's docstring")
    PATH = property(get_path, set_path, del_path, "PATH's docstring")
    PARITY = property(get_parity, set_parity, del_parity, "PARITY's docstring")
    RTSCTS = property(get_rtscts, set_rtscts, del_rtscts, "RTSCTS's docstring")
    TIMEOUT = property(get_timeout, set_timeout, del_timeout, "TIMEOUT's docstring")
    XONXOFF = property(get_xonxoff, set_xonxoff, del_xonxoff, "XONXOFF's docstring")
    WAIT_MEASURE = property(get_wait_measure, set_wait_measure, del_wait_measure, "WAIT_MEASURE's docstring")
    ERRORCODE = property(get_errorcode, set_errorcode, del_errorcode, "ERRORCODE's docstring")
    OUT = property(get_out, set_out, del_out, "OUT's docstring")
    NAME = property(get_name, set_name, del_name, "NAME's docstring")
    SERIAL_NUMBER = property(get_serial_number, set_serial_number, del_serial_number, "SERIAL_NUMBER's docstring")
    SIGNAL_DELAY = property(get_signal_delay, set_signal_delay, del_signal_delay, "SIGNAL_DELAY's docstring")
    RETURNCODE = property(get_returncode, set_returncode, del_returncode, "RETURNCODE's docstring")
    ADDRESS = property(get_address, set_address, del_address, "ADDRESS's docstring")
