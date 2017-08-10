#!/usr/bin/python3
__author__ = 'Jakub Pelikan'
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango
from multiple_monitors import __version__
from multiple_monitors.pages.page import Page

class AboutPage(Page):

    def init(self):
        #application name
        about_title_label = Gtk.Label(self._('Multiple Monitors'))
        pango_font = Pango.FontDescription("Sans 40")
        about_title_label.modify_font(pango_font)
        self.attach(about_title_label, 0,3,0,2)
        #Description
        self.create_label(self._('\t Gui application for multiple monitors manage.\n '),[0,3,2,3],self, alignment='center')
        #version
        self.create_label(self._('Version:'),[0,1,3,4],self, alignment='right')
        self.create_label(__version__,[1,3,3,4],self, alignment='left')
        #author
        self.create_label(self._('Author:'),[0,1,4,5],self, alignment='right')
        self.create_label(self._('Jakub Pelikan'),[1,3,4,5],self, alignment='left')
        #nick
        self.create_label(self._('Nick:'),[0,1,5,6],self, alignment='right')
        self.create_label(self._('P-eli'),[1,3,5,6],self, alignment='left')
        #email
        self.create_label(self._('Email:'),[0,1,6,7],self, alignment='right')
        self.create_label(self._('jakub.pelikan@gmail.com'),[1,3,6,7],self, alignment='left')
        #Website
        self.create_label(self._('Website:'),[0,1,7,8],self, alignment='right')
        website = Gtk.Label()
        self.create_label('',[1,3,7,8],self,website, alignment='left')
        website.set_markup("<a href=\"http://github.com/p-eli/multiple-monitors\" " "title=\"Click to open website\">http://github.com/p-eli/multiple-monitors</a>")
        self.create_label('',[0,1,8,9],self, alignment='right')
        self.create_label('',[0,1,9,10],self, alignment='right')



