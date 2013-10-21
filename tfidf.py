from _hashlib import new

__author__ = 'Pawel Rychly, Dawid Wisniewski'


class TfIdf:

    __documents = []
    __idfs = {}
    __inverted_file = []
    __tf = []

    def __init__(self):
        return

    def init_documents_collection(self, filename):
        self.__documents = []
        file = open(filename)
        try:
            line = file.readline()
            while line:
                #self.__documents.extend(line.split())
                self.__documents.append(line.strip())
                line = file.readline()
        except IOError:
            print "Error: can\'t find file or read data"
        finally:
            file.close()
        return

    def __print_vocabulary(self):
        for item in self.__idfs.items():
            print item[0] + " idf = " + item[1]

    def print_documents(self):
        for index, document in enumerate(self.__documents):
            print "doc {0}: {1}".format(index, document)

tfidf = TfIdf()
tfidf.init_documents_collection("data//documents.txt")
tfidf.print_documents()


