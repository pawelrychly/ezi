#!/usr/bin/env python

import pygtk
pygtk.require('2.0')

#pygtk.require('2.0')
import gtk
from tfidf import TfIdf
from results_view import ResultView
from query_expander_view import QueryExpanderView
from QueryExpander import QueryExpander
import nltk


class GUI:

    __directories = {
        "Documents": "data//documents-lab1.txt",
        "Keywords": "data//keywords-lab1.txt"
    }

    def do_search(self, widget, data):
        query = self.entry.get_text()
        result = self.tfidf.rank(query)
        self.result_view.show_documents(result)
        if self.is_query_expanding_active:
            new_queries = self.query_expander.expand(query)
            list = []
            for new_query in new_queries:
                if len(new_query) >= 1:
                    list.append(" ".join(new_query))
            self.query_expander_view.show_queries(list)

        #self.text_area.get_buffer().set_text(self.tfidf.get_result())
        
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def show_keywords(self):
        self.keywords_area.get_buffer().set_text(self.tfidf.get_keywords_string())

    def toggle_query_expanding(self, widget):
        self.is_query_expanding_active = not self.is_query_expanding_active
        if self.is_query_expanding_active:
            self.query_expander_container.show()
        else:
            self.query_expander_container.hide()
            self.query_expander_view.remove_old_buttons()
        print self.is_query_expanding_active

    def open_file(self, widget,  name):
        text = "Select {0} Source File".format(name)
        filechooserdialog = gtk.FileChooserDialog(text, None, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))
        response = filechooserdialog.run()

        if response == gtk.RESPONSE_OK:
            self.__directories[name] = filechooserdialog.get_filename()
            self.tfidf = TfIdf(self.__directories['Documents'], self.__directories['Keywords'])
            self.query_expander = QueryExpander()
            self.query_expander.loadKeywords(self.__directories['Keywords'])
            print "directories"
            print self.__directories
            #self.tfidf.print_stemmed_keywords()
            self.show_keywords()

        filechooserdialog.destroy()

    def __init__(self):
        self.query_expander = QueryExpander()
        self.query_expander.loadKeywords(self.__directories['Keywords'])
        #inits window and connects delete event
        print gtk.pygtk_version
        self.is_query_expanding_active = True
        self.tfidf = TfIdf(self.__directories['Documents'], self.__directories['Keywords'])
        print 'Dokument', self.tfidf.print_documents()
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
        self.box1.pack_start(self.get_query_expander_view(), True, True, 0)
        self.box1.pack_start(self.get_result_layaut(), True, True, 0)
        self.box1.pack_start(document_view, True, True, 0)
        self.box1.pack_start(self.get_keywords_layout(), True, True, 0)
        self.show_keywords()
        #self.tfidf.print_stemmed_keywords()
        self.window.show_all()

    def get_query_expander_view(self):
        box = gtk.VBox()
        check_box = gtk.CheckButton("Query Expanding")
        check_box.set_active(True)
        check_box.connect("clicked", self.toggle_query_expanding)
        box.pack_start(check_box, False, False, 0)
        self.query_expander_container = gtk.ScrolledWindow()
        self.query_expander_container.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.query_expander_view = QueryExpanderView(self)
        self.query_expander_container.add_with_viewport(self.query_expander_view)
        box.pack_start(self.query_expander_container, True, True, 0)

        return box

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
        self.similar_list = []
        hbox = gtk.HBox(False, 5)
        self.entry = gtk.Entry()

        completion = gtk.EntryCompletion()
        self.liststore = gtk.ListStore(str)

        self.entry.set_completion(completion)
        completion.set_model(self.liststore)
        completion.set_text_column(0)

        for item in self.similar_list:
            self.liststore.append([item])



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