"""
Sudoku solver using backtracking search on a constraint satisfaction problem
"""

import sys
import argparse
import itertools
from csp import CSP, BacktrackSearch

def same_row(square1, square2):
	return (square1[0] == square2[0])

def same_col(square1, square2):
	return (square1[1] == square2[1])

def same_3x3(square1, square2):
	same_three_row = (square1[0] / 3 == square2[0] / 3)
	same_three_col = (square1[1] / 3 == square2[1] / 3)
	return (same_three_row and same_three_col)

def make_sudoku_csp(given_assignment):
	""" Creates the CSP with Sudoku restrictions
	given_assignment	the original puzzle, maps coordinates (r, c) to digits
	"""
	csp = CSP()
	for row in range(9):
		for col in range(9):
			csp.add_variable((row, col), range(1, 10))
	for square in given_assignment:
		csp.add_unary_factor(square, lambda s: (s == given_assignment[square]))
	for s1 in itertools.product(range(9), range(9)):
		for s2 in itertools.product(range(9), range(9)):
			if s1 == s2:
				continue
			if same_row(s1, s2) or same_col(s1, s2) or same_3x3(s1, s2):
				csp.add_binary_factor(s1, s2, lambda v1, v2: (v1 != v2))
	return csp

def print_no_newline(s):
	sys.stdout.write(str(s))

def output_sudoku(assignment):
	""" Formats the Sudoku solution
	assignment		the solution, maps coordinates (r, c) to digits
	"""
	assert (len(assignment.keys()) == 81)
	for row in range(9):
		for col in range(9):
			print_no_newline(assignment[(row, col)]) 
			if col % 3 == 2:
				print_no_newline(' ')
		print ''
		if row % 3 == 2:
			print ''
	print ''

def solve_sudoku(raw_puzzle, output_all):
	""" Makes and executes the backtracking Sudoku solver, outputs the results
	raw_puzzle			list of strings, representing the rows of the puzzle
						'?' represents a blank square
	output_all			boolean representing whether to print all solutions
						(if False, we only print the first solution)
	"""
	partial_assignment = { (row, col): int(raw_puzzle[row][col]) for row \
		in range(9) for col in range(9) if raw_puzzle[row][col] != '?' }
	csp = make_sudoku_csp(partial_assignment)
	solver = BacktrackSearch(csp)
	solver.solve()
	solutions = solver.get_solutions()
	if len(solutions) == 1:
		print 'There is 1 solution.'
	else:
		print 'There are {0} solutions.'.format(len(solutions))
	if len(solutions) > 0:
		print 'The first solution is: '
		output_sudoku(solutions[0])
		if not output_all or len(solutions) == 1:
			return
		print 'The remaining solutions are: '
		for i in range(1, len(solutions)):
			output_sudoku(solutions[i])

def input_sudoku(infile):
	""" Takes the Sudoku puzzle from file input
	"""
	if infile == sys.stdin:
		print '\nInput one row at a time, using question marks for the blanks'
		print 'Terminate with CTRL-D'
	raw_puzzle = [''.join(line.split()) for line in infile]
	return raw_puzzle

def main():
	parser = argparse.ArgumentParser(description='Sudoku solver based on '\
		'solving a CSP')
	parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), \
		default=sys.stdin, help='Optional input file')
	parser.add_argument('-a', '--all', action='store_true')
	args = parser.parse_args()
	raw_puzzle = input_sudoku(args.infile)
	solve_sudoku(raw_puzzle, args.all)

if __name__ == '__main__':
	main()
