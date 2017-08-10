#!/usr/bin/python3
from gi.repository import Gtk
from multiple_monitors.userSetting import UserSetting


class Page(Gtk.Table):
    def __init__(self, parent):
        Gtk.Table.__init__(self, 10, 3, True)
        self.parent = parent
        self._setting = UserSetting()
        self._ = self._setting.gettext
        self.set_border_width(20)
        self.set_row_spacings(10)
        self.set_col_spacings(10)
        self.init()

    @staticmethod
    def create_button(text, pos, table, action, button=None):
        if text:
            if not button:
                button = Gtk.Button.new_with_mnemonic(text)
            else:
                button.set_label(text)
        button.connect("clicked", action)
        table.attach(button, pos[0], pos[1], pos[2], pos[3])

    @staticmethod
    def create_label(text, pos, table, interface_label=None, alignment='right'):
        if not interface_label:
            interface_label = Gtk.Label(text)
        else:
            try:
                interface_label.set_text(text)
            except:
                interface_label.set_text('None')
        if alignment == 'right':
            interface_label.set_alignment(1, 0.5)
        elif alignment == 'left':
            interface_label.set_alignment(0, 0.5)
        elif alignment == 'center':
            interface_label.set_alignment(0.5, 0.5)
        table.attach(interface_label, pos[0], pos[1], pos[2], pos[3])

    @staticmethod
    def create_combo_box(name, pos, table, default=None):
        renderer_text = Gtk.CellRendererText()
        name.pack_start(renderer_text, True)
        name.add_attribute(renderer_text, "text", 0)
        if default:
            name.set_active(default)
        table.attach(name, pos[0],pos[1],pos[2],pos[3])

    @staticmethod
    def create_entry(name, pos, table, text="", visible=True):
        name.set_text(text)
        name.set_visibility(visible)
        table.attach(name, pos[0], pos[1], pos[2], pos[3])

    @staticmethod
    def create_check_button(name, pos, table, action, check=True):
        name.set_active(check)
        name.connect("clicked", action)
        table.attach(name, pos[0], pos[1], pos[2], pos[3])

    @staticmethod
    def create_switch_button(pos, table, function, active=True):
        switch = Gtk.Switch()
        switch.connect("notify::active", function)
        switch.set_active(active)
        table.attach(switch, pos[0], pos[1], pos[2], pos[3])

    @staticmethod
    def get_combo_box_select(combo_box):
        tree_iter = combo_box.get_active_iter()
        if tree_iter:
            model = combo_box.get_model()
            return (model[tree_iter][0])
        return None

    @staticmethod
    def send_error_dialog(parent, primary_text, secondary_text):
        dialog = Gtk.MessageDialog(parent, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, primary_text)
        dialog.format_secondary_text(secondary_text)
        dialog.run()
        dialog.destroy()

    @staticmethod
    def create_text_view_column(treeview, names):
        renderer = Gtk.CellRendererText()
        id = 0
        for name in names:
            column_name = Gtk.TreeViewColumn(name, renderer, text=id)
            column_name.set_sort_column_id(id)
            treeview.append_column(column_name)
            id += 1
