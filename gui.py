#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
from tfidf import TfIdf
from results_view import ResultView

class GUI:

    __directories = {
        "Documents": "data//documents.txt",
        "Keywords": "data//keywords.txt"
    }

    def do_search(self, widget, data):
        query = self.entry.get_text()
        result = self.tfidf.rank(query)
        self.result_view.show_documents(result)
        #self.text_area.get_buffer().set_text(self.tfidf.get_result())
        
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def show_keywords(self):
        self.keywords_area.get_buffer().set_text(self.tfidf.get_keywords_string())


    def open_file(self, widget,  name):
        text = "Select {0} Source File".format(name)
        filechooserdialog = gtk.FileChooserDialog(text, None, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))
        response = filechooserdialog.run()

        if response == gtk.RESPONSE_OK:
            self.__directories[name] = filechooserdialog.get_filename()
            self.tfidf = TfIdf(self.__directories['Documents'], self.__directories['Keywords'])
            print self.__directories
            self.tfidf.print_stemmed_keywords()
            self.show_keywords()

        filechooserdialog.destroy()

    def __init__(self):
        #inits window and connects delete event
        self.tfidf = TfIdf(self.__directories['Documents'], self.__directories['Keywords'])
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Czesc Milosz!")
        self.window.connect("delete_event", self.delete_event)
        self.window.set_default_size(600,500)
        self.window.set_border_width(5)
        
        #prepare layout
        self.box1 = gtk.VBox(False, 5)
        self.window.add(self.box1)
        document_view = self.get_document_textarea_layout()
        self.box1.pack_start(self.get_menu_box(), False, False, 0)
        self.box1.pack_start(self.get_search_panel_layout(), False, False, 0)
        self.box1.pack_start(self.get_result_layaut(), True, True, 0)
        self.box1.pack_start(document_view, True, True, 0)
        self.box1.pack_start(self.get_keywords_layout(), True, True, 0)
        self.show_keywords()
        self.tfidf.print_stemmed_keywords()
        self.window.show_all()

    def get_menu_box(self):
        #menu
        mb = gtk.MenuBar()

        filemenu = gtk.Menu()
        file_item = gtk.MenuItem("File")
        file_item.set_submenu(filemenu)

        open_document_item = gtk.MenuItem("Open Documents Source")
        open_document_item.connect("activate", self.open_file, "Documents")

        open_keywords_item = gtk.MenuItem("Open Keywords Source")
        open_keywords_item.connect("activate", self.open_file, "Keywords")

        exit_item = gtk.MenuItem("Exit")
        exit_item.connect("activate", gtk.main_quit)

        filemenu.append(open_document_item)
        filemenu.append(open_keywords_item)
        filemenu.append(exit_item)

        mb.append(file_item)
        return mb

    def get_search_panel_layout(self):
        #prepare layout
        hbox = gtk.HBox(False, 5)
        self.entry = gtk.Entry()
        hbox.pack_start(self.entry, True, True, 0)
        #prepare search button
        btn_search = gtk.Button("Szukaj")
        btn_search.connect("clicked", self.do_search, "button 2")
        hbox.pack_start(btn_search, True, True, 0)
        return hbox

    def get_result_layaut(self):
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.result_view = ResultView(self.document_area)
        sw.add_with_viewport(self.result_view)

        #prepare text area for results
        #self.text_area = gtk.TextView()
        #sw = gtk.ScrolledWindow()
        #sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        #self.text_area = gtk.TextView()
        #sw.add(self.text_area)
        return sw

    #def get_bottomarea_layout(self):
        #bottom = gtk.HBox(False, 0)
        #bottom.pack_start(self.get_document_textarea_layout(), False, False, 0)
        #bottom.pack_start(self.get_keywords_layout(), False, False, 0)
        #return bottom

    def get_document_textarea_layout(self):
        #prepare text area for results
        frame = gtk.Frame()
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.document_area = gtk.TextView()
        sw.add(self.document_area)
        frame.set_label("Document:")
        frame.add(sw)
        return frame

    def get_keywords_layout(self):
        #prepare text area for results
        frame = gtk.Frame()
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.keywords_area = gtk.TextView()
        sw.add(self.keywords_area)
        frame.set_label("Keywords:")
        frame.add(sw)
        return frame


def main():
    gtk.main()

if __name__ == "__main__":
    hello = GUI()
    main()