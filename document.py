__author__ = 'Pawel Rychly, Dawid Wisniewski'
from PorterStemmer import PorterStemmer

class Document:
    __text = ''
    __stemmed_text = ''
    __title = ''

    def __init__(self, title, text):
        self.__text = text
        self.__stemmed_text = self.__stem_text(text)
        self.__title = title

    def __stem_text(self, text):
        p = PorterStemmer()
        stemmed_text = ''
        word = ''
        for c in text:
            if c.isalpha():
                word += c.lower()
            else:
                if word:
                    stemmed_text += p.stem(word, 0,len(word)-1)
                    word = ''
                if c.lower() == ' ':
                    stemmed_text += c.lower()
        return stemmed_text

    def get_stemmed_document(self):
        return self.__stemmed_text

    def get_document(self):
        return self.__text

    def get_title(self):
        return self.__title;
