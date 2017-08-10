#!/usr/bin/python3
import pickle
import os

config_file_name = 'config'


class UserSetting(object):
    __instance = None
    _language = 'English_en'
    _home_dir = None
    displaylink = False
    def __new__(cls):

        if not UserSetting.__instance:
            UserSetting.__instance = object.__new__(cls)
            config_file = os.path.join( UserSetting.__instance.home_dir, config_file_name)
            if os.path.exists(config_file):
                UserSetting.__instance = UserSetting.__instance.load(UserSetting.__instance)
            else:
                pass
        return UserSetting.__instance

    def __init__(self):
        self._language_list = ['English_en'] # todo

    def load(self):
        config = pickle.load(os.path.join(self._setting.home_dir, config_file_name))
        return config

    def save(self):
        with open(os.path.join(self._home_dir, config_file_name)) as file:
            pickle.dump(self, file)

    def gettext(self, text):
        return text

    @property
    def language_list(self):
        return self._language_list

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, lang):
        for l in self._language_list:
            if lang in l:
                self._language = l
                break

    @property
    def home_dir(self):
        if not self._home_dir:
            try:
                self._home_dir = os.path.join(os.path.expanduser("~" + os.getenv("SUDO_USER")), 'multipleMonitors')
            except:
                self._home_dir = os.path.join(os.path.expanduser("~" + os.getlogin()), 'multipleMonitors')
        return self._home_dir

    @staticmethod
    def get_icon_path():
        root = __file__
        if os.path.islink(root):
            root = os.path.realpath(root)
        path = os.path.dirname(os.path.abspath(root))
        return (os.path.join(path, "icon.png"))