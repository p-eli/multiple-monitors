#!/usr/bin/python3
from multiple_monitors.pages.page import Page
from multiple_monitors.userSetting import UserSetting
from multiple_monitors.profiles import Profiles
from multiple_monitors.profile  import Profile
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

SCALE_FACTOR = 8
class EditorPage(Page):
    def init(self):
        self._setting = UserSetting()
        self._profiles = Profiles()
        self.active_monitors=[]
        # initialize profile selection
        self.create_label(self._('Select profile'), [0, 1, 0, 1], self, alignment='right')
        self.profile_combo_box = Gtk.ComboBox.new_with_model(self.create_profile_list_store())
        default_position = self._profiles.get_profiles_name().index(self._profiles.get_current_profile_name())
        self.profile_combo_box.connect("changed", self.change_profile)
        self.create_combo_box(self.profile_combo_box, [1, 3, 0, 1], self, default_position)
        # initialize monitor layout
        self.init_monitor_layout(self._profiles.get_current_profile().monitors)
        # save, delete, apply button
        self.create_button(self._('Delete'), [0, 1, 9, 10], self, self.remove_profile)
        self.create_button(self._('Apply'), [1, 2, 9, 10], self, self.apply_profile)
        self.create_button(self._('Save'), [2, 3, 9, 10], self, self.save_profile)

    def create_profile_list_store(self):
        profile_list_store = Gtk.ListStore(str)
        for profile in self._profiles.profiles:
            profile_list_store.append([profile.name])
        return profile_list_store

    def init_monitor_layout(self, monitors):
        self.monitor_layout = Gtk.Layout()
        frame = Gtk.Frame()
        frame.add(self.monitor_layout)
        frame.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("grey"))
        self.attach(frame, 0, 3, 1, 9)
        self.create_monitors(monitors)

    def create_monitors(self, monitors):
        for monitor in monitors:
            if monitor.status == "connected":
                self.active_monitors.append(MonitorLabel(monitor, self.monitor_layout))
        self.show_all()

    def change_profile(self, button):
        for monitor in self.active_monitors:
            monitor.destroy()
        profile_name = self.get_combo_box_select(self.profile_combo_box)
        profile = self._profiles.get_profile_by_name(profile_name)
        self.create_monitors(profile.monitors)

    def remove_profile(self, button):
        text = self.get_combo_box_select(self.profile_combo_box)
        if text != "Default":
            self._profiles.remove_profile(text)

    def apply_profile(self, button):
        name = self.get_combo_box_select(self.profile_combo_box)
        self._profiles.apply_profile(Profile(name, self.get_monitor_list(), self._setting.displaylink))

    def save_profile(self, button):
        text = self.get_combo_box_select(self.profile_combo_box)
        if text == "Default":
            messagedialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.OK,
                                              self._("Set Profile Name"))
            action_area = messagedialog.get_content_area()
            entry = Gtk.Entry()
            action_area.pack_start(entry, True, True, 0)
            messagedialog.show_all()
            messagedialog.run()
            name = entry.get_text()
            messagedialog.destroy()
        self._profiles.save_profile(Profile(name, self.get_monitor_list(), self._setting.displaylink))

    def get_monitor_list(self):
        monitor_list = []
        for monitor in self.active_monitors:
            monitor_list.append(monitor.monitor)
        return monitor_list

class MonitorLabel(Gtk.Label):
    def __init__(self, monitor,  layout):
        Gtk.Label.__init__(self)
        self.monitor = monitor
        self.drag = False
        self.drag_x = 0
        self.drag_y = 0
        self.layout = layout
        self.x = 0
        self.y = 0
        self.set_monitor_label()

        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("white"))

        self.frame = Gtk.Frame()
        self.frame.add(self)
        self.set_size_request(monitor.resolution_x/SCALE_FACTOR, monitor.resolution_y/SCALE_FACTOR)
        self.event_box = Gtk.EventBox()
        self.event_box.set_visible_window(False)
        self.event_box.add(self.frame)
        self.event_box.connect("button-release-event", self.release)
        self.event_box.connect("button-press-event", self.click)
        self.event_box.connect("motion-notify-event", self.mousemove)
        self.layout.put(self.event_box, monitor.position_x/SCALE_FACTOR, monitor.position_y/SCALE_FACTOR)
        self.create_menu(True, monitor.primary,  monitor.available_resolution,
                         str(self.monitor.resolution_x)+"x"+str(self.monitor.resolution_y))


    def create_menu(self, active, primary, resolution, active_resolution):
        self.menu = Gtk.Menu()
        prim = Gtk.CheckMenuItem("Primary")
        prim.set_active(primary)
        prim.connect("activate", self.menu_change_stat_primary)
        self.menu.append(prim)

        act = Gtk.CheckMenuItem("Active")
        act.set_active(active)
        act.connect("activate", self.menu_change_stat_active)
        self.menu.append(act)

        res_submenu = Gtk.Menu()
        menu = None
        for r in resolution:
            title = str(r[0])+"x"+str(r[1])
            menu = Gtk.RadioMenuItem(title, group=menu)
            if title == active_resolution:
                menu.set_active(True)
            menu.connect("activate", self.menu_change_resolution, r[0], r[1])
            res_submenu.append(menu)
        res = Gtk.MenuItem("Resolution")

        res.set_submenu(res_submenu)
        self.menu.append(res)
        self.menu.show_all()

    def set_monitor_label(self):
        if self.monitor.primary:
            text = "<span color='black'><b>"+self.monitor.name+"</b> \nPrimary</span>"
        else:
            text = "<span color='black'><b>" + self.monitor.name + "</b></span>"
        self.set_markup(text)

    def menu_change_stat_primary(self, widget):
        self.monitor.primary = widget.get_active()
        self.set_monitor_label()

    def menu_change_stat_active(self, widget):
        self.monitor.status = "disconnected"
        self.destroy()

    def menu_change_resolution(self, widget, res_x, res_y):
        self.monitor.resolution_x = res_x
        self.monitor.resolution_y = res_y
        self.set_size_request(self.monitor.resolution_x / SCALE_FACTOR, self.monitor.resolution_y / SCALE_FACTOR)


    def click(self, widget, event):
        if event.button == 1:  # drag
            self.drag = True
            self.drag_x = event.x
            self.drag_y = event.y
        elif event.button == 3:  # show menu
            self.menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())


    def release(self, widget, event):
        if self.drag:
            self.monitor.position_x = (self.x + int(event.x - self.drag_x))*SCALE_FACTOR
            self.monitor.position_y = (self.x + int(event.x - self.drag_x))*SCALE_FACTOR
        self.drag = False

    def mousemove(self, widget, event):
        if self.drag:
            self.layout.move(self.event_box, self.x + int(event.x - self.drag_x), self.y + int(event.y - self.drag_y))
            self.x, self.y = self.layout.child_get(self.event_box, 'x', 'y')