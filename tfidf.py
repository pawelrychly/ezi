from stemmer_helper import StemmerHelper
from document import Document
from math import log, pow, sqrt

__author__ = 'Pawel Rychly, Dawid Wisniewski'


class TfIdf:

    __documents = []
    __idfs = {}
    __inverted_file = {}
    __tf = []
    __keywords = set()
    __search_result = []

    def __init__(self, documents_filename, keywords_filename):
        self.__inverted_file = {}
        self.__search_result = []
        self.__keywords = set()
        self.__search_result = []
        self.__tf = []
        self.__documents = []
        self.__init_keywords(keywords_filename)
        self.__init_documents_collection(documents_filename)
        self.__init_values()
        #self.rank("weka, resource")
        #self.print_result()
        return

    def print_result(self):
        print "SEARCHING RESULT"
        for document in self.__search_result:
            print "{0}, {1}".format(document.get_score(), document.get_title())

    def get_keywords_string(self):
        return "\r\n".join(self.__keywords)

    def get_result(self):
        data = []
        for document in self.__search_result:
            data.append("{0}, {1}".format(document.get_score(), document.get_title()))
        return "\r\n".join(data)

    def __init_keywords(self, keywords_filename):
        print keywords_filename
        self.__documents = []
        #p = PorterStemmer()
        file = open(keywords_filename)
        try:
            line = file.readline()
            while line:
                stemmed_word = StemmerHelper.stem_text(line)
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
        print "documents filename: {0}".format(documents_filename)
        file = open(documents_filename)
        try:
            title = ''
            line = file.readline()
            text = ''
            while line:
                print line
                if title == '':
                    title = line
                text += line + ' '
                if line and line.isspace():
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

    def print_documents(self):
        for index, document in enumerate(self.__documents):
            print "doc title {0}:\n {1}".format(index, document.get_title())
            print "doc stemmed {0}:\n {1}".format(index, document.get_stemmed_document())

    def __get_tf(self, text):
        term_freqs = {}
        max = 0.0
        terms = text.split()
        for term in terms:
            if term in self.__keywords:
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
            term_freqs = self.__get_tf(document.get_stemmed_document())
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


            if not (number_of_documents_with_term == 0):
                #print "num of all docs {0}".format(number_of_all_documents)
                #print "num of docs with term {0}".format(number_of_documents_with_term)
                idf = log(float(number_of_all_documents) / float(number_of_documents_with_term))
            self.__idfs[term] = idf

    def rank(self, query):
        query = StemmerHelper.stem_text(query)
        term_freqs = self.__get_tf(query)
        query_vector = {}
        for term, tf in term_freqs.iteritems():
            idf = 0.0
            if self.__idfs.has_key(term):
                idf = self.__idfs[term]
            tfidf = tf * idf
            print "{0} tf {1} : idf {2} : {3}".format(term, tf, idf, tfidf )
            query_vector[term] = tfidf

        union = set()
        for term in term_freqs.keys():
            if self.__inverted_file.has_key(term):
                union = union | self.__inverted_file[term]
        scores = []
        for id in union:
            scores.append({'id': id, 'score': self.__similarity(query_vector, self.__get_document_vector(id))})

        sorted_scores = sorted(scores, key=lambda k: k['score'], reverse=True)
        self.__search_result = []
        for score in sorted_scores:
            document = self.__documents[score['id']]
            document.set_score(score['score'])
            self.__search_result.append(document)

        return self.__search_result



    def __get_document_vector(self, document_id):
        if document_id < len(self.__tf):
            vector = {}
            term_freqs = self.__tf[document_id]
            for term, tf in term_freqs.iteritems():
                tfidf = tf * self.__idfs[term]
                vector[term] = tfidf
        return vector

    def __similarity(self, vector_a, vector_b):
        sum = 0.0
        for term, tfidf_a in vector_a.iteritems():
            if vector_b.has_key(term):
                tfidf_b = vector_b[term]
                sum += tfidf_a * tfidf_b

        t = self.__vector_length(vector_a) * self.__vector_length(vector_b)
        print self.__vector_length(vector_a)
        print self.__vector_length(vector_b)
        print "t: {0}".format(t)
        result = 0.0
        if t != 0.0:
            result = sum / t
        return result

    def __vector_length(self, vector):
        sum = 0.0
        for term, value in vector.iteritems():
            sum += pow(value, 2)
        l = sqrt(sum)
        return l

#tfidf = TfIdf("data//documents.txt", "data//keywords.txt")



