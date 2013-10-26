import sys
from nltk import wordnet as wn
# niezalezne rezultaty od keywords.txt
# podobienstwo miedzy keywordsami i wybor najbardziej podobnych
# podobienstwo miedzy nowym a keywordsami


class QueryExpander:
	def expand(self, query):
		query_candidates = [] #list of candidate queries after expansion
		query = query.replace('(,|\.|\n)', '') #remove dots, commas and newlines
		query_parts = query.split() #split on whitespaces to obtain token list
		
		word_similarities = []
		for word in query_parts[:3]: #get first 3 words (should be most meaningful )
			word_similarities.append(self._getMostSimilarKeyword(word))
		print word_similarities

	def loadKeywords(self, filepath):
		f = open(filepath, 'r')
		keywords = dict()

		for line in f:
			keywords[line.strip()] = wn.wordnet.synsets(line.strip()) # set word -> synonymes relation
			
		self.keywords = keywords

	def _getMostSimilarKeyword(self, query_word):
		synsets = wn.wordnet.synsets(query_word) # get synonymes of query word
		if len(synsets) == 0:
			print 'Cannot find word: ', query_word, 'in wordnet!' 
			return ''


		#find word that is closest to our query word 
		best_similarity = 0.0
		best_keyword    = '';

		for keyword in self.keywords.keys(): # iterate through every keyword from file
			if len(self.keywords[keyword]) > 0: # if contains some data in wordnet
				if self.keywords[keyword][0].pos == synsets[0].pos and keyword != query_word: #if keyword is in wordnet and with the same postag
					similarity = synsets[0].lch_similarity(self.keywords[keyword][0])
					if similarity > best_similarity:
						best_similarity = similarity
						best_keyword = keyword
		return best_keyword

qe = QueryExpander()
qe.loadKeywords('./data/keywords-2.txt')

qe.expand(sys.argv[1])