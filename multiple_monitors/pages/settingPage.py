#!/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from multiple_monitors.pages.page import Page
from multiple_monitors.userSetting import UserSetting


class SettingPage(Page):

    def init(self):
        #language label
        self._setting = UserSetting()
        self.create_label(self._('Language'), [0, 1, 0, 1], self, alignment='right')
        #init language comboBox
        self.language_combo_box = Gtk.ComboBox.new_with_model(self.create_language_list_store())
        default_position = self._setting.language_list.index(self._setting.language)
        self.create_combo_box(self.language_combo_box, [1, 3, 0, 1], self, default_position)
        # init display link
        self.create_label(self._('Use DisplayLink'), [0, 1, 1, 2], self, alignment='right')
        self.create_switch_button([2,3,1,2], self, self.display_link, self._setting.displaylink)
        #Automatic check update
        # self.create_label(self._('Automatic update'),[0,1,1,2],self, alignment='right')
        # self.create_switch_button([2,3,1,2], self, self.automatic_check_update, self.setting['userSetting'].version['autoCheck'])
        #save
        self.create_button(self._('Save'), [2, 3, 9, 10], self, self.save_setting)

    def save_setting(self, button=None):
        self._setting.language = self.get_combo_box_select(self.language_combo_box)
        self._setting.save()

    def create_language_list_store(self):
        language_list_store = Gtk.ListStore(str)
        for item in self._setting.language_list:
            language_list_store.append([item])
        return language_list_store

    def display_link(self, switch, gparam):
        if switch.get_active():
            self._setting.displaylink = True
        else:
            self._setting.displaylink = False

    # def automatic_check_update(self, switch, gparam):
    #     if switch.get_active():
    #         self.setting['userSetting'].version['autoCheck'] = True
    #     else:
    #         self.setting['userSetting'].version['autoCheck'] = False
