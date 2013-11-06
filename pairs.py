import sys
import nltk
from nltk.corpus import wordnet
import os

class QueryExpander:
	def remove_stopwords(self, data, stopwords):
		result = []
		for item in data:
			isOK = True
			for stopword in stopwords:
				if stopword == item:
					isOK = False
					break
			if isOK:
				result.append(item)
		return result

	def getBigramsCount(self, inputfile, stopfile):
		f = open(inputfile, 'r')
		stoplist = open(stopfile, 'r')
		stopwords = []

		data = f.read()
		data = data.strip()
		data = data.replace("(.|,|!)", " ")
		data = data.lower()
		tokens = data.split()
		
		for line in stoplist:
			stopwords.append(line.strip())

		tokens = self.remove_stopwords(tokens, stopwords)
		bigrams = nltk.bigrams(tokens)
		occurences = dict()
		for bigram in bigrams:
			if bigram in occurences:
				occurences[bigram] += 1
			else:
				occurences[bigram] = 1 
		trimmed = dict() 
		for (a,b) in occurences.keys():
			if occurences[(a,b)] > 1 and a.isalpha() and b.isalpha():
				trimmed[(a,b)] = occurences[(a,b)]
		return trimmed

	def expand(self, query_word):
		files_list =  os.listdir('./dat')
		result_dict = dict()
		for f in files_list:
			trimmed = self.getBigramsCount('./dat/'+f, 'stoplist')
			result_dict = dict(result_dict.items() + trimmed.items())

		#for (a,b) in result_dict:
		#	print (a,b), result_dict[(a,b)]
		for (a,b) in result_dict:
			if a == query_word or b == query_word:
				print a, b, result_dict[(a,b)]

expander = QueryExpander()
expander.expand(sys.argv[1])