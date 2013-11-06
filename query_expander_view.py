__author__ = 'Pawel Rychly Dawid Wisniewski'

import pygtk
pygtk.require('2.0')
import gtk
from tfidf import TfIdf

class QueryExpanderView(gtk.VButtonBox):

    def __init__(self, entry):
        super(QueryExpanderView, self).__init__()
        self.__all_buttons = []
        self.queries = []
        self.entry = entry
        self.tooltips = gtk.Tooltips()
        self.set_layout(gtk.BUTTONBOX_START)

    def chose_query(self, widget, query):
        self.entry.set_text(query)

    def append_query(self, query):
        title = query
        button = gtk.Button(title)
        button.connect("clicked", self.chose_query, query)
        self.pack_start(button, gtk.TRUE, gtk.TRUE, 0)
        self.tooltips.set_tip(button, "Wybierz zapytanie")
        self.__all_buttons.append(button)

    def show_queries(self, queries):
        self.remove_old_buttons()
        for query in queries:
            self.append_query(query)
        self.show_all()

    def remove_old_buttons(self):
        for button in self.__all_buttons:
            self.remove(button)
        for i in range(len(self.__all_buttons)):
            button = self.__all_buttons.pop()