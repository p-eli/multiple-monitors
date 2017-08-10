#!/usr/bin/python3


class MonitorController(object):
    __instance = None
    _default_config = None

    def __new__(cls):
        if not MonitorController.__instance:
            MonitorController.__instance = object.__new__(cls)
        return MonitorController.__instance

    def __init__(self):
        if not self._default_config:
            self.create_default_profile()

    def unplug_all(self):
        pass

    def unplug(self, monitor_id):
        pass

    def create_default_profile(self):
        pass