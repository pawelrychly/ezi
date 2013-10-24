#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
from tfidf import TfIdf
class GUI:

    def do_search(self, widget, data):
        query = self.entry.get_text()
        self.tfidf.rank(query)
        self.text_area.get_buffer().set_text(self.tfidf.get_result())
        
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self):
        #inits window and connects delete event
        self.tfidf = TfIdf("data//documents.txt", "data//keywords.txt")
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Czesc Milosz!")
        self.window.connect("delete_event", self.delete_event)
        self.window.set_border_width(5)
        
        #prepare layout
        self.box1 = gtk.VBox(False, 0)
        self.window.add(self.box1)

        #entry for writing our query
        self.entry = gtk.Entry()
        self.box1.pack_start(self.entry, True, True, 0)
        self.entry.show()

        #prepare search button
        self.btn_search = gtk.Button("Szukaj")
        self.btn_search.connect("clicked", self.do_search, "button 2")
        self.box1.pack_start(self.btn_search, True, False, 0)
        self.btn_search.show()
        
        #prepare text area for results
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