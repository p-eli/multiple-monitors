#!/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from multiple_monitors.userSetting import UserSetting
from multiple_monitors.pages.aboutPage import AboutPage
from multiple_monitors.pages.settingPage import SettingPage
from multiple_monitors.pages.editorPage import EditorPage
class MainWindow(Gtk.Window):
    __instance = None
    _setting = None

    def __new__(cls):
        if not MainWindow.__instance:
            MainWindow.__instance = Gtk.Window.__new__(cls)
        return MainWindow.__instance

    def __init__(self):
        if not self._setting:
            Gtk.Window.__init__(self, title='Multiple Monitors')
            self._setting = UserSetting()
            self._ = self._setting.gettext
            self.set_border_width(3)
            self.notebook = Gtk.Notebook()
            self.add(self.notebook)
            self.set_default_icon_from_file(self._setting.get_icon_path())
            self.init_pages()
            self.show_all()

    def init_pages(self):
        editor_page = EditorPage(self)
        self.notebook.append_page(editor_page, Gtk.Label(self._('Edit')))

        setting_page = SettingPage(self)
        self.notebook.append_page(setting_page, Gtk.Label(self._('Setting')))

        about_page = AboutPage(self)
        self.notebook.append_page(about_page, Gtk.Label(self._('About')))

    def change_page(self, page):
        pass


