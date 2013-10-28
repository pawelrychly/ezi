__author__ = 'Pawel Rychly Dawid Wisniewski'

import pygtk
pygtk.require('2.0')
import gtk
from tfidf import TfIdf

class ResultView(gtk.VButtonBox):

    def __init__(self, textarea):
        super(ResultView, self).__init__()
        self.__all_buttons = []
        self.document_textarea = textarea
        self.tooltips = gtk.Tooltips()

    def show_document(self, widget,  document):
        self.document_textarea.get_buffer().set_text(document.get_stemmed_document())

    def append_document(self, document):
        title = "{0}    {1}".format(document.get_score(), document.get_title())
        button = gtk.Button(title)
        button.connect("clicked", self.show_document, document)
        self.pack_start(button, gtk.TRUE, gtk.TRUE, 0)
        self.tooltips.set_tip(button, "Nacisnij aby zobaczyc zawartosc")
        self.__all_buttons.append(button)

    def show_documents(self, documents):
        self.remove_old_buttons()
        for document in documents:
            self.append_document(document)
        self.show_all()

    def remove_old_buttons(self):
        for button in self.__all_buttons:
            self.remove(button)
        for i in range(len(self.__all_buttons)):
            button = self.__all_buttons.pop()