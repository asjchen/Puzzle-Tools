import sys
import fileinput

MIN_WORD_LENGTH = 3
HORIZONTAL_OK = True
VERTICAL_OK = True
DIAGONAL_OK = True
BACKWARDS_OK = False
UPWARDS_OK = True

f = open('/usr/share/dict/words', 'r')
word_dict = [word.lower() for word in f.read().split()]
ws_list = [line.lower().strip() for line in fileinput.input()]

def make_trie(words):
    root = dict()
    for word in words:
        current_dict = root
        for letter in word:
            current_dict = current_dict.setdefault(letter, {})
        current_dict['_end_'] = '_end_'
    return root

def in_trie(trie, word):
    current_dict = trie
    for letter in word:
        if letter in current_dict:
            current_dict = current_dict[letter]
        else:
            return False
    else:
        if '_end_' in current_dict:
            return True
        else:
            return False

wst = make_trie(word_dict)

def find_horizontal_words(backword_words, word_arr):
    final_words = set()
    for line in word_arr:
        for i in range(len(line)):

            # Backward words
            if backword_words:
                for j in range(i):
                    word = line[j:i + 1]
                    if len(word) >= MIN_WORD_LENGTH and in_trie(wst, word):
                        final_words.add(word)

            # Forward words
            for j in range(i + 1, len(line)):
                word = line[i: j + 1]
                if len(word) >= MIN_WORD_LENGTH and in_trie(wst, word):
                    final_words.add(word)
    return final_words

print find_horizontal_words(BACKWARDS_OK, ws_list)

def find_vertical_words(upward_words, word_arr):
    vert_array = []
    for j in range(len(word_arr[0])):
        string = ""
        for i in range(len(word_arr)):
            string += ws_list[i][j]
        vert_array.append(string)
    return find_horizontal_words(upward_words, vert_array)

print find_vertical_words(UPWARDS_OK, ws_list)








