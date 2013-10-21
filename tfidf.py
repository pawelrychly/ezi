__author__ = 'Paweł Rychły, Dawid Wiśniewski'


class TfIdf:

    __documents = []
    __idfs = {}
    __inverted_file = []
    __tf = []

    def __init__(self):
        return

    def __init_documents_collection(self, filename):
        self.__documents = []
        file = open(filename)
        try:
            line = file.readline()
            self.__documents.extend(line.split())
        except IOError:
            print "Error: can\'t find file or read data"
        finally:
            file.close()

        return

