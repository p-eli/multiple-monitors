#!/usr/bin/python3
__author__ = 'Jakub Pelikan'


class Profile(object):
    # name = None
    # monitors = []
    # display_link = False

    def __init__(self, name, monitors, display_link=False):
        self.name = name
        self.monitors = monitors
        self.display_link = display_link
    # @property
    # def name(self):
    #     return self._name
    #
    # @ name.setter
    # def name(self, value):
    #     self._name = value
    #

