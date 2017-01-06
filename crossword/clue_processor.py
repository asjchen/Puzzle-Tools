

CLUE_FILE = 'clue_answer_data/clues.txt'

def process_clues(filename):
	f = open(filename, 'r')
	lines = f.readlines()
	clue_data = {}	

	for line in lines:
		line_data = line.split(' ')
		line_data = line_data[:-2] # remove temporal data
		clue_data[line_data[:-1]] = line_data[-1]



