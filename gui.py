#!/usr/bin/env python

# example helloworld2.py

import pygtk
pygtk.require('2.0')
import gtk

class GUI:

    def callback(self, widget, data):
        print "Hello again - %s was pressed" % data
        self.text_area.set_editable(True)
        self.text_area.get_buffer().set_text("CZESC MILOSZ")
        #self.text_area.Buffer.Text = "HELLOW"

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Czesc Milosz!")
        self.window.connect("delete_event", self.delete_event)

        self.window.set_border_width(5)
        
        self.box1 = gtk.VBox(False, 0)
        self.window.add(self.box1)

        self.entry = gtk.Entry()
        self.box1.pack_start(self.entry, True, True, 0)
        self.entry.show()

        self.button2 = gtk.Button("Button 2")
        self.button2.connect("clicked", self.callback, "button 2")
        self.box1.pack_start(self.button2, True, False, 0)
        self.button2.show()
        
        self.text_area = gtk.TextView()
        self.box1.pack_start(self.text_area, True, True, 0)
        self.text_area.show()

        self.box1.show()
        self.window.show()

def main():
    gtk.main()

if __name__ == "__main__":
    hello = GUI()
    main()