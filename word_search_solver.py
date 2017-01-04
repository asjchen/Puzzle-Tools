import sys
import fileinput
 
MIN_WORD_LENGTH = 4

# HORIZONTAL DIRECTIONS

HORIZONTAL_FORWARDS_OK = True
HORIZONTAL_BACKWARDS_OK = True

# VERTICAL DIRECTIONS

VERTICAL_DOWN_OK = True
VERTICAL_UP_OK = True

# DIAGONAL DIRECTIONS

DIAGONAL_DR_OK = True # diagonal down-right
DIAGONAL_UR_OK = True # diagonal up-right
DIAGONAL_DL_OK = True # diagonal down-left
DIAGONAL_UL_OK = True # diagonal up-left



################# TRIE FUNCTIONS #################

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

########################################################



def find_horizontal_words(valid_directions, word_arr, wst):
    final_words = set()
    for row in range(len(word_arr)):
        line = word_arr[row]
        for i in range(len(line)):

            # Backward words
            if valid_directions[1]:
                for j in range(i + 1):
                    word = line[j:i + 1][::-1]
                    if len(word) >= MIN_WORD_LENGTH and in_trie(wst, word):
                        final_words.add((word, (row, i)))

            # Forward words
            if valid_directions[0]:
                for j in range(i + 1, len(line)):
                    word = line[i: j + 1]
                    if len(word) >= MIN_WORD_LENGTH and in_trie(wst, word):
                        final_words.add((word, (row, i)))
    return final_words

def find_vertical_words(valid_directions, word_arr, wst):
    final_words = set()
    for row in range(len(word_arr)):
        rows_below = len(word_arr) - row - 1
        for col in range(len(word_arr[0])):

            # Vertical Down
            if valid_directions[0]:
                word = ''
                for i in range(rows_below + 1):
                    word += word_arr[row + i][col]
                    if len(word) >= MIN_WORD_LENGTH and in_trie(wst, word):
                        final_words.add((word, (row, col)))

            # Vertical Up
            if valid_directions[1]:
                word = ''
                for i in range(row + 1):
                    word += word_arr[row - i][col]
                    if len(word) >= MIN_WORD_LENGTH and in_trie(wst, word):
                        final_words.add((word, (row, col)))
    return final_words


def find_diagonal_words(valid_directions, word_arr, wst):
    final_words = set()
    for row in range(len(word_arr)):
        rows_below = len(word_arr) - row - 1
        for col in range(len(word_arr[0])):
            columns_right = len(word_arr[0]) - col - 1

            # Diagonal Down-Right
            if valid_directions[0]:
                word = ''
                for i in range(min(columns_right, rows_below) + 1):
                    word += word_arr[row + i][col + i]
                    if len(word) >= MIN_WORD_LENGTH and in_trie(wst, word):
                        final_words.add((word, (row, col)))

            # Diagonal Down-Left
            if valid_directions[1]:
                word = ''
                for i in range(min(col, rows_below) + 1):
                    word += word_arr[row + i][col - i]
                    if len(word) >= MIN_WORD_LENGTH and in_trie(wst, word):
                        final_words.add((word, (row, col)))

            # Diagonal Up-Left
            if valid_directions[2]:
                word = ''
                for i in range(min(col, row) + 1):
                    word += word_arr[row - i][col - i]
                    if len(word) >= MIN_WORD_LENGTH and in_trie(wst, word):
                        final_words.add((word, (row, col)))

            # Diagonal Up-Right
            if valid_directions[3]:
                word = ''
                for i in range(min(columns_right, row) + 1):
                    word += word_arr[row - i][col + i]
                    if len(word) >= MIN_WORD_LENGTH and in_trie(wst, word):
                        final_words.add((word, (row, col)))

    return final_words


def main():
    f = open('/usr/share/dict/words', 'r')
    word_dict = [word.lower() for word in f.read().split()]
    wst = make_trie(word_dict)

    print "Input each line of the word search on a separate line"
    print "Enter the letters, pressing ENTER after each line and pressing CTRL+D at the end"

    ws_list = [''.join(line.lower().split()) for line in fileinput.input()]
    print '\n', "Processing..."

    valid_horizontal_directions = [HORIZONTAL_FORWARDS_OK, HORIZONTAL_BACKWARDS_OK]
    horizontal_words = find_horizontal_words(valid_horizontal_directions, ws_list, wst)

    valid_vertical_directions = [VERTICAL_DOWN_OK, VERTICAL_UP_OK]
    vertical_words = find_vertical_words(valid_vertical_directions, ws_list, wst)

    valid_diagonal_directions = [DIAGONAL_DR_OK, DIAGONAL_DL_OK, DIAGONAL_UL_OK, DIAGONAL_UR_OK]
    diagonal_words = find_diagonal_words(valid_diagonal_directions, ws_list, wst)

    words = list(horizontal_words) + list(vertical_words) + list(diagonal_words)
    words = sorted(words)

    print "Processed!"

    print "Word", '\t\t', "Row", '\t', "Column"
    print "---------------------------------"
    for (word, (row, col)) in words:
        print word, '\t\t', row, '\t', col


if __name__ == '__main__':
    main()






