"""
Indexing Words
Given a list of words w1, w2, ..., wn, this script finds the words v1, v2, ..., vm
such that for each word vi, the first letter lies in w1, the second in w2, etc
"""

import sys
import itertools

def main():
	all_combos = False
	f = open('/usr/share/dict/words', 'r')
	word_dict = [word.lower() for word in f.read().split()]
	f.close()
	word_list = [word.lower() for word in sys.stdin.read().split()]
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
	print solns

if __name__ == '__main__':
	main()






