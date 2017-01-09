
"""
Used for processing tagged clue data and reducing using Porter Stemming
"""

import nltk
import pickle
from nltk.stem import *
from nltk.stem.porter import *
from location_globals import *

def porter_stem(tagged_filename, verbose=False):
	f = open(tagged_filename, 'rb')
	tagged_data = pickle.load(f)
	f.close()

	stemmer = PorterStemmer()

	new_data = {}
	for key in tagged_data:
		key_as_list = list(key)
		
		new_key = []
		for (word, pos) in key_as_list:
			new_word = stemmer.stem(word)

			if verbose: print word, "-->", new_word
			
			new_key.append((new_word, pos))
		new_data[tuple(new_key)] = tagged_data[key]

	return new_data


def main():
	stemmed_data = porter_stem(TAGGED_CLUE_FILE, False)
	f = open(STEMMED_CLUE_FILE, 'wb')
	pickle.dump(stemmed_data, f)
	f.close()


if __name__ == '__main__':
	main()




