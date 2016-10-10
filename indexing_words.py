# PuzzleHunt Tools
# Given a list of words w1, w2, ..., wn, this script finds the words v1, v2, ..., vm
# such that for each word vi, the first letter lies in w1, the second in w2, etc

import sys

f = open('/usr/share/dict/words', 'r')
word_dict = [word.lower() for word in f.read().split()]
word_list = [word.lower() for word in sys.stdin.read().split()]
solns = []
for word in word_dict:
	if len(word) == len(word_list):
		is_valid = True
		for i in range(len(word)):
			is_valid = is_valid and (word[i] in list(word_list[i]))
		if is_valid:
			solns.append(word)
print solns






