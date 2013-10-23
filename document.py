__author__ = 'Pawel Rychly, Dawid Wisniewski'
from stemmer_helper import StemmerHelper

class Document:
    __text = ''
    __stemmed_text = ''
    __title = ''
    __score = 0.0

    def __init__(self, title, text):
        self.__text = text
        self.__stemmed_text = StemmerHelper.stem_text(text)
        self.__title = title
        self.__score = 0.0

    def get_stemmed_document(self):
        return self.__stemmed_text

    def get_document(self):
        return self.__text

    def get_title(self):
        return self.__title;

    def set_score(self, value):
        self.__score = value

    def get_score(self):
        return self.__score