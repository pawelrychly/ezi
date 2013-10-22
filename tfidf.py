from _hashlib import new
from PorterStemmer import PorterStemmer
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
            document = ""
            p = PorterStemmer()
            output = ''
            while line:
                #self.__documents.extend(line.split())
                word = ''

                for c in line:
                    if c.isalpha():
                        word += c.lower()
                    else:
                        if word:
                            output += p.stem(word, 0,len(word)-1)
                            word = ''
                        if c.lower() == ' ':
                            output += c.lower()

                if len(line) == 1:
                    #print output
                    self.__documents.append(output)
                    output = ''
                line = file.readline()
        except IOError:
            print "Error: can\'t find file or read data"
        finally:
            file.close()
        return

    def get_tf(self, term, doc_id):
        try:
            freq = self.tf[doc_id][doc_id]
        except:
            return 0
        return freq


    def __print_vocabulary(self):
        for item in self.__idfs.items():
            print item[0] + " idf = " + item[1]

    def print_documents(self):
        for index, document in enumerate(self.__documents):
            print "doc {0}: {1}".format(index, document)

    def init(self):
        return



tfidf = TfIdf()
tfidf.init_documents_collection("data//documents.txt")
tfidf.print_documents()
print tfidf.get_tf("Aha", 0)


