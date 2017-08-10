#!/usr/bin/python3
import os
import pickle
import copy
from multiple_monitors.userSetting import UserSetting
from multiple_monitors.xrand import Xrand
from multiple_monitors.profile import Profile


class Profiles(object):
    __instance = None
    _default_profile = None
    _profiles = []
    _home_dir = None
    _current = None
    _xrandr = None
    _screen = None
    def __new__(cls):
        if not Profiles.__instance:
            Profiles.__instance = object.__new__(cls)
        return Profiles.__instance

    def __init__(self):
        self._setting = UserSetting()
        self._xrandr = Xrand()
        if not self._default_profile:
            self.load_profiles()
            self.create_default_profile()
            self._current = copy.deepcopy(self._default_profile)

    def open_profile(self, name):
        profile = pickle.load(os.path.join(self._setting.home_dir, name))
        return profile

    def save_profile(self, profile):
        with open(os.path.join(self._home_dir, profile.name)) as file:
            pickle.dump(profile, file)

    def load_profiles(self):
        if os.path.isdir(self._setting.home_dir):
            for profile in os.listdir(self._setting.home_dir):
                self._profiles.add(self.open_profile(profile))

    def remove_profile(self, name):
        os.remove(os.path.join(self._setting.home_dir, name))

    def get_profile_by_name(self, name):
        for profile in self.profiles:
            if profile.name == name:
                return profile
        return self._default_profile


    def get_current_profile_name(self):
        return self._current.name

    def get_current_profile(self):
        return self._current

    def restore_default(self):
        self._current = copy.deepcopy(self._default_profile)
        self.apply_profile(self._default_profile)

    def unplug(self, monitor_id):
        for monitor in self._current.monitors:
            if monitor.name == monitor_id:
                monitor.status = False
                self.apply_profile(self._current)

    def create_default_profile(self):
        actual_monitors, self._screen = self._xrandr.load_from_x()
        for prof in self._profiles:
            if set(prof.monitors).intersection(actual_monitors):
                self._default_profile = prof
                return
        profile = Profile('Default', actual_monitors, self._setting.displaylink)
        self._default_profile = profile

    def get_monitors(self):
        return self._current.monitors

    def get_monitors_list(self):
        monitors, _ = self._xrandr.load_from_x()
        monitors_name = []
        for m in monitors:
            monitors_name.append(m.name)
        return monitors_name

    def get_profiles_name(self):
        names = []
        for prof in self.profiles:
            names.append(prof.name)
        return names

    def apply_profile(self, profile):
        self._xrandr.apply_profile(profile.monitors, profile.display_link)

    @property
    def profiles(self):
        if not self._profiles:
            self.load_profiles()
            if self._default_profile.name == "Default":
                self._profiles.append(self._default_profile)
        return self._profiles






