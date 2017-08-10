#!/usr/bin/python3
from multiple_monitors.tray import Tray
from multiple_monitors.userSetting import UserSetting
from multiple_monitors.mainWindow import MainWindow
from multiple_monitors.monitorsController import MonitorController
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MultipleMonitors(object):
    def __init__(self):
        setting = UserSetting()
        if not os.path.isdir(setting.home_dir):  # first start
            self.first_start(setting)
        self.tray = Tray()
        Gtk.main()

    def first_start(self, setting):
        os.mkdir(setting.home_dir)
        setting.save()
        MainWindow()

if __name__ == "__main__":
    app = MultipleMonitors()
