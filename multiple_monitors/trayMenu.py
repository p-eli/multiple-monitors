#!/usr/bin/python3
from multiple_monitors.profiles import Profiles
from multiple_monitors.mainWindow import MainWindow
from multiple_monitors.userSetting import UserSetting

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class TrayMenu(Gtk.Menu):
    def __init__(self, event_button, event_time):
        Gtk.Menu.__init__(self)
        self._profiles = Profiles()
        self._setting = UserSetting()
        self._ = self._setting.gettext
        self.init_menu()
        self.popup(None, None, None, None, event_button, event_time)
        self.show_all()

    def init_menu(self):
        current = self.create_menu_item(self._profiles.get_current_profile_name())
        current.set_sensitive(False)
        self.create_separator()
        self.create_menu_item(self._("Show Layout"), self.window_action)
        self.create_menu_item(self._("New profile"), self.window_action)
        item = []
        for prof in self._profiles.profiles:
            item.append([prof.name, True])
        self.create_submenu(self._("Select profile"), item, self.apply_profile)
        item = []
        for mon in self._profiles.get_monitors():
            item.append([mon.name, mon.status=="connected"])
        self.create_submenu(self._("Unplug"), item, self.unplug)
        self.create_menu_item(self._("Restore default"), self.restore_default)
        self.create_separator()
        self.create_menu_item(self._('About'), self.window_action)
        self.create_menu_item(self._('Setting'), self.window_action)
        self.create_menu_item(self._('Exit'), self.exit_action)

    def create_menu_item(self, text, action=None, menu=None, item=None, enable=True):
        if not item:
            item = Gtk.MenuItem(text)
        if not menu:
            self.append(item)
        else:
            menu.append(item)
        if action:
            item.connect('activate', action)
        item.set_sensitive(enable)
        return item

    def create_submenu(self, text, items, action):
        submenu = Gtk.Menu()
        submenu_item = Gtk.MenuItem(self._(text))
        submenu_item.set_submenu(submenu)
        self.append(submenu_item)
        if items:
            for item in items:
                self.create_menu_item(item[0], action, submenu, enable=item[1])

        else:
            empty = self.create_menu_item(self._("Empty"), None, submenu)
            empty.set_sensitive(False)

    def restore_default(self, button):
        self._profiles.restore_default()

    def unplug(self, button):
        self._profiles.unplug(button.get_label())

    def apply_profile(self, button):
        self._profiles.apply_profile(self._profiles.get_profile_by_name(button.get_label()))

    def create_separator(self):
        separator = Gtk.SeparatorMenuItem()
        self.append(separator)

    def window_action(self, button):
        win = MainWindow()
        leg = {self._("Show Layout"): 0, self._("New profile"): 1, self._('Setting'): 3, self._('About'): 4}
        win.change_page(leg[button.get_label()])
        win.show()

    def exit_action(self, button=None):
        Gtk.main_quit(button)
        exit()

