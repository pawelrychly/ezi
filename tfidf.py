from _hashlib import new
from PorterStemmer import PorterStemmer
from document import Document
from math import log

__author__ = 'Pawel Rychly, Dawid Wisniewski'


class TfIdf:

    __documents = []
    __idfs = {}
    __inverted_file = {}
    __tf = []
    __keywords = set()

    def __init__(self, documents_filename, keywords_filename):
        self.__init_keywords(keywords_filename)
        self.print_stemmed_keywords()
        self.__init_documents_collection(documents_filename)
        self.__init_values()
        self.print_idfs()
        self.print_tfs("resourc")
        return

    def __init_keywords(self, keywords_filename):
        self.__documents = []
        p = PorterStemmer()
        file = open(keywords_filename)
        try:
            line = file.readline()
            while line:
                word = ''
                stemmed_word = ''
                for c in line:
                    if c.isalpha():
                        word += c.lower()
                    else:
                        if word:
                            stemmed_word += p.stem(word, 0,len(word)-1)
                            word = ''
                if len(stemmed_word) > 0:
                    self.__keywords.add(stemmed_word)
                line = file.readline()
        except IOError:
            print "Error: can\'t find keywords file or read data"
        finally:
            file.close()
        return

    def print_stemmed_keywords(self):
        for word in self.__keywords:
            print word

    def __init_documents_collection(self, documents_filename):
        self.__documents = []
        file = open(documents_filename)
        try:
            title = ''
            line = file.readline()
            text = ''
            while line:
                if title == '':
                    title = line
                text += line + ' '
                if len(line) == 1:
                    document = Document(title, text)
                    text = ''
                    title = ''
                    self.__documents.append(document)
                line = file.readline()
        except IOError:
            print "Error: can\'t find documents file or read data"
        finally:
            file.close()
        return

    def print_idfs(self):
        for term, idf in self.__idfs.iteritems():
            print "idf {0}: {1}".format(term, idf)

    def print_tfs(self, term):
        for id, document in enumerate(self.__documents):
            if self.__tf[id].has_key(term):
                print "{0} : tf  {1}: {2}".format(id, term, self.__tf[id][term])

    #def get_tf(self, term, doc_id):
    #    try:
    #        freq = self.tf[doc_id][doc_id]
    #    except:
    #        return 0
    #    return freq

    def print_documents(self):
        for index, document in enumerate(self.__documents):
            print "doc title {0}:\n {1}".format(index, document.get_title())
            print "doc stemmed {0}:\n {1}".format(index, document.get_stemmed_document())

    def __get_tf(self, document):
        term_freqs = {}
        max = 0.0
        terms = document.get_stemmed_document().split()
        for term in terms:
            count = 1.0;
            if term_freqs.has_key(term):
                count = term_freqs[term]
                count += 1.0
            term_freqs[term] = count
            if count > max:
                max = count

        for term, value in term_freqs.iteritems():
            term_freqs[term] = value/max
        return term_freqs

    def get_tf(self, term, document_id):
        if document_id < len(self.__tf):
            if self.__tf[document_id].has_key(term):
                return self.__tf[document_id][term]
        return 0.0

    def __init_values(self):
        document_id = 0
        for document in self.__documents:
            term_freqs = self.__get_tf(document)
            self.__tf.append(term_freqs)
            for term in term_freqs.keys():
                ids = set()
                if self.__inverted_file.has_key(term):
                    ids = self.__inverted_file[term]
                ids.add(document_id)
                self.__inverted_file[term] = ids
            document_id +=1

        for term, document_ids in self.__inverted_file.iteritems():
            number_of_documents_with_term = len(document_ids)
            number_of_all_documents = len(self.__documents)
            idf = 0.0
            if number_of_documents_with_term != 0.0:
                idf = log(number_of_all_documents / number_of_documents_with_term)
            self.__idfs[term] = idf

tfidf = TfIdf("data//documents.txt", "data//keywords.txt")
#tfidf.print_documents()


