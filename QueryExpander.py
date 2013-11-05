import sys
from nltk import wordnet as wn
import math
# niezalezne rezultaty od keywords.txt
# podobienstwo miedzy keywordsami i wybor najbardziej podobnych
# podobienstwo miedzy nowym a keywordsami


class QueryExpander:
	def expand(self, query):
		query = query.replace('(,|\.|\n)', '') #remove dots, commas and newlines
		query_parts = query.split() #split on whitespaces to obtain token list
		
		word_similarities = []
		for word in query_parts[:3]: #get first 3 words (should be most meaningful )
			word_similarities.append(self._getMostSimilarKeyword(word))
		candidates = self.generateCombinations(query_parts[:3], word_similarities)
		full_candidates = []

		for candidate in candidates:
			full_candidates.append(self._recreate_query(candidate, query_parts))
		return full_candidates

	def loadKeywords(self, filepath):
		f = open(filepath, 'r')
		keywords = dict()

		for line in f:
			keywords[line.strip()] = wn.wordnet.synsets(line.strip()) # set word -> synonymes relation
			
		self.keywords = keywords

	def generateCombinations(self, input_query_list, candidate_query_list):
		possibilities = 2**len(candidate_query_list)
		results = []

		for i in range(possibilities):
			one_result = []
			for j in range(int(math.log(possibilities, 2))):
				if i & (2**j) == 0:
					one_result.append(input_query_list[j])
				else:
					one_result.append(candidate_query_list[j])
			results.append(one_result)
		return results

	def _recreate_query(self, query_candidate, input_query_list):
		return query_candidate + input_query_list[3:]

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

result = qe.expand(sys.argv[1])
for item in result:
	print item