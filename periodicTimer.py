#!/usr/bin/env python

import gtk, gobject

class PerodicTimer:
    def __init__(self, timeout):

        # create a simple window with a label
        self.window = gtk.Window()
        self.window.connect('destroy', lambda wid: gtk.main_quit())
        self.window.connect('delete_event', lambda a1,a2:gtk.main_quit())
        vbox = gtk.VBox()
        self.window.add(vbox)
        self.label = gtk.Label('Periodic Timer')
        vbox.pack_start(self.label)
        self.window.show_all()

        # register a periodic timer
        self.counter = 0
        gobject.timeout_add_seconds(timeout, self.callback)

    def callback(self):
        self.label.set_text('Counter: ' + str(self.counter))
        self.counter += 1
        return True

if __name__ == '__main__':
    periodic_timer = PerodicTimer(1)
    gtk.main()