# Puzzle-Tools

This repo contains a variety of programs for solving puzzles and is developed by Nicholas Hirning and Andy Chen

### The Tools ###

- Word Indexer (indexing_words.py): given a list of words, finds words taking one letter from each word in the list (in the list order)
- Word Search Solver (word\_search\_solver.py): input the word search and find all possible words
- TODO: Sudoku, regular crosswords, ...

### Acknowledgments ###
To check if words are valid, we will use either the internal word list (for our MacBooks this is located at /usr/share/dict/words), a corpus of 100k common English words taken from https://gist.github.com/h3xx/1976236, or a corpus of 10k common English words taken from https://github.com/first20hours/google-10000-english.

Crossword data is pulled from https://github.com/donohoe/nyt-crossword. For more information view the readme in crossword/clue\_answer\_data/.

The CSP class (used in the Sudoku solver and crossword solver) and all related algorithms are based off of code taken from the Stanford University CS 221 course.
