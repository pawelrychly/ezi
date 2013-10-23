__author__ = 'Pawel Rychly, Dawid Wisniewski'
from PorterStemmer import PorterStemmer

class StemmerHelper:
    @staticmethod
    def stem_text(text):
        p = PorterStemmer()
        stemmed_text = ''
        word = ''
        for i, c in enumerate(text):
            if c.isalpha():
                word += c.lower()
            if not c.isalpha() or i == (len(text) - 1):
                if word:
                    stemmed_text += p.stem(word, 0,len(word)-1)
                    word = ''
                if c.lower() == ' ':
                    stemmed_text += c.lower()
        return stemmed_text