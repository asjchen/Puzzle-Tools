
"""
Used for processing raw clue data into tagged clue data
"""

import nltk
import pickle
from location_globals import *

# Potential Issue: 	- clues with _ or - as in "Turn-___ (thrills)"
#					- clues with parentheses or Abbr.
#					- clues with quotes (some have double/triple quotes)
#					- clues with possession (e.g., Aaron's cat)

####################################################
############ Processing Raw --> Tagged #############
####################################################

def process_nyt_clues_text(filename):
	# return dictionary from tuple of tokenized clues to result 

	f = open(filename, 'rU') # universal newline support
	lines = f.readlines()
	f.close()
	clue_data = {}	

	for line in lines:
		line_data = line.split()
		line_data = line_data[:-2] # remove temporal data
		clue_data[tuple(line_data[:-1])] = line_data[-1]

	return clue_data

def tagging_pos(clue_data, verbose = False):
	result = {}
	if verbose: counter = 0
	for clue in clue_data:
		clue_tagged = nltk.pos_tag(clue)
		result[tuple(clue_tagged)] = clue_data[clue]

		if verbose:
			if counter % 1000 == 0:
				print "Processed", counter, "Words"
			counter += 1

	return result

def process_nyt_to_tagged(in_filename, out_filename, verbose = False):
	clue_data = process_nyt_clues_text(in_filename)
	tagged_data = tagging_pos(clue_data, verbose)
	f = open(out_filename, 'wb')
	pickle.dump(tagged_data, f)
	f.close()

def main():
	process_nyt_to_tagged(RAW_CLUE_FILE, TAGGED_CLUE_FILE, True)


if __name__ == '__main__':
	main()




