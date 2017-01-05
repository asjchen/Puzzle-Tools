# Puzzle-Tools

This repo contains a variety of programs for solving puzzles and is developed by Nicholas Hirning and Andy Chen

### The Tools ###

- Word Indexer (indexing_words.py): given a list of words, finds words taking one letter from each word in the list (in the list order)
- Word Search Solver (word_search_solver.py): input the word search and find all possible words
- TODO: Sudoku, cryptic crosswords, regular crosswords, ...

### Word Dictionaries ###
To check if words are valid, we will use either the internal word list (for our MacBooks this is located at /usr/share/dict/words) or a corpus of 100k common English words taken from https://gist.github.com/h3xx/1976236.
