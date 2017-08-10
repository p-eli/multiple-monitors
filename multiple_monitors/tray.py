#!/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from multiple_monitors.mainWindow import MainWindow
from multiple_monitors.trayMenu import TrayMenu
from multiple_monitors.userSetting import UserSetting

class Tray(Gtk.StatusIcon):
    def __init__(self):
        Gtk.StatusIcon.__init__(self)
        self.init()

    def init(self):
        self.set_from_file(UserSetting().get_icon_path())
        self.connect('popup-menu', self.on_right_click)
        self.connect('activate', self.on_left_click)

    @staticmethod
    def on_right_click(self, event_button, event_time):
        self.rightClick = TrayMenu(event_button, event_time)

    @staticmethod
    def on_left_click(self):
        MainWindow().show()




