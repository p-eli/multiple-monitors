#!/usr/bin/python3

class Monitor(object):
    name = None
    status = "disconnected"
    _position_x = 0
    _position_y = 0
    _available_resolution = []
    _resolution_x = 0
    _resolution_y = 0
    primary = False
    rotate = 'normal'

    def __init__(self, name):
        self.name = name

    @property
    def position(self):
        return str(self._position_x)+"x"+str(self._position_y)

    @property
    def resolution(self):
        return str(self._resolution_x) + "x" + str(self._resolution_y)

    @property
    def position_x(self):
        return self._position_x

    @position_x.setter
    def position_x(self, value):
        self._position_x = int(value)

    @property
    def position_y(self):
        return self._position_y

    @position_y.setter
    def position_y(self, value):
        self._position_y = int(value)

    @property
    def resolution_x(self):
        return self._resolution_x

    @resolution_x.setter
    def resolution_x(self, value):
        self._resolution_x = int(value)

    @property
    def resolution_y(self):
        return self._resolution_y

    @resolution_y.setter
    def resolution_y(self, value):
        self._resolution_y = int(value)

    @property
    def available_resolution(self):
        return self._available_resolution

    @available_resolution.setter
    def available_resolution(self, value):
        self._available_resolution = value