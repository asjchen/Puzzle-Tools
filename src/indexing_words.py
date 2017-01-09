"""
Indexing Words
Given a list of words w1, w2, ..., wn, this script finds the words v1, v2, ..., vm
such that for each word vi, the first letter lies in w1, the second in w2, etc
"""

import sys
from os import path
from inspect import getsourcefile
import argparse
import itertools

def make_parser():
	parser = argparse.ArgumentParser(description='Given a word list, ' \
		'finds a word such that the nth letter comes from the nth word')
	parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), \
		default=sys.stdin, help='Optional input file')
	source_file = path.abspath(getsourcefile(lambda: 0))
	tool_dir = path.dirname(path.dirname(source_file))
	google_dict = path.join(tool_dir, 'word_lists', 'google-10000-english.txt')
	parser.add_argument('-d', '--dict', type=argparse.FileType('r'), \
		default=google_dict, \
		help='Word dictionary, consisting of possible words to spell,' \
		'defaults to the Google 10000 English list')
	parser.add_argument('-a', '--all_orders', action='store_true', \
		help='Toggles whether the word list can be permuted ' \
		'(i.e. whether the word list is not sorted')
	return parser

def index_words(word_dict, word_list, all_combos):
	solns = []
	if all_combos:
		orders = itertools.permutations(word_list)
	else:
		orders = [word_list]
	for order in orders:
		for word in word_dict:
			if len(word) == len(order):
				is_valid = True
				for i in range(len(word)):
					is_valid = is_valid and (word[i] in list(order[i]))
				if is_valid:
					solns.append(word)
					print word
	return solns

def main():
	parser = make_parser()
	args = parser.parse_args()
	word_dict = [word.lower() for word in args.dict.read().split()]
	args.dict.close()
	if args.infile == sys.stdin:
		print 'Enter each word on a new line, terminating with CTRL-D'
	word_list = [word.lower() for word in args.infile.read().split()]
	args.infile.close()
	print index_words(word_dict, word_list, args.all_orders)

if __name__ == '__main__':
	main()






