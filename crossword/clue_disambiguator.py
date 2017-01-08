# Uses word sense disambiguation to label each word in each hint
# 

import nltk
from word_sense_disambiguation import *
import pickle
from nltk.stem import *
from nltk.stem.porter import *
from location_globals import *

cache = {}

def fill_cache(data):

	for clue_item in data:
		new_sentence = []
		sentence = [clue for (clue, pos) in clue_item]
		parts_of_speech = [pos for (clue, pos) in clue_item]
		
		for i in range(len(sentence)):
			synset = lesk(sentence, sentence[i], parts_of_speech[i])
			print synset
			new_sentence.append(synset)

		cache[tuple(new_sentence)] = data[clue_item]


def main():
	f = open(STEMMED_CLUE_FILE, 'rb')
	current_data = pickle.load(f)
	f.close()

	fill_cache(current_data)
	print cache
	
	


if __name__ == '__main__':
	main()