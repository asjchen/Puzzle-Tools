"""
Classes for creating and solving constraint satisfaction problems (CSP's) with
factor graphs. Here, we only use unary and binary factors, as we can decompose 
general n-ary factors into unary and binary factors
"""

import copy

class CSP:
	"""
	Class to support constraint satisfaction problems as factor graphs,
	with unary and/or binary factors
	"""
	def __init__(self):
		"""
		vars			list of unique, hashable objects
		domains			maps each var to a list of possible values
		unary_factors	maps each var to a dictionary of val: factor(val);
						in other words, unary_factors[var][val] = factor(val)
		binary_factors	maps each var1 to a dictionary with keys var2;
						each binary_factors[var1][var2] is a table so that
						binary_factors[var1][var2][val1][val2] = 
						factor(val1, val2)
		"""
		self.vars = []
		self.domains = {}
		self.unary_factors = {}
		self.binary_factors = {}

	def add_variable(self, var, domain):
		"""
		var			hashable object not already in self.vars
		domain		list of possible values for var
		"""
		assert (var not in self.vars)
		self.vars.append(var)
		self.domains[var] = domain[:]
		self.unary_factors[var] = None
		self.binary_factors[var] = dict()

	def add_unary_factor(self, var, new_factor):
		"""
		var			hashable object in self.vars
		new_factor	numerical function that takes any value for var 
		"""
		if self.unary_factors[var] == None:
			self.unary_factors[var] = {val: float(new_factor(val)) for val \
				in self.domains[var]}
		else:
			for val in self.domains[var]:
				assert (val in self.unary_factors[var])
				self.unary_factors[var][val] *= new_factor(val)

	def add_binary_factor(self, var1, var2, new_factor):
		"""
		var1, var2		distinct hashable objects in self.vars
		new_factor		numerical function that takes any value for var1 and 
						any value for var2 
		"""
		assert (var1 != var2)
		new_table_var1 = {val1: {val2: new_factor(val1, val2) for val2 \
			in self.domains[var2]} for val1 in self.domains[var1]}
		self.update_binary_table(var1, var2, new_table_var1)
		new_table_var2 = {val2: {val1: new_factor(val1, val2) for val1 \
			in self.domains[var1]} for val2 in self.domains[var2]}
		self.update_binary_table(var2, var1, new_table_var2)

	def update_binary_table(self, var1, var2, new_table):
		""" Helper function for add_binary_factor
		var1, var2		distinct hashable objects in self.vars
		new_table		dictionary so that 
						new_table[val1][val2] = new_factor(val1, val2)
		"""
		if var2 not in self.binary_factors[var1]:
			self.binary_factors[var1][var2] = new_table
		else:
			for val1 in self.domains[var1]:
				assert (val1 in self.binary_factors[var1][var2])
				for val2 in self.domains[var2]:
					assert (val2 in self.binary_factors[var1][var2][val1])
					new_mult = new_table[val1][val2]
					self.binary_factors[var1][var2][val1][val2] *= new_mult

class BacktrackSearch:
	def __init__(self, csp):
		"""
		solutions			list of pairs (full assignment, weight)
		csp					deep copy of the CSP to solve
		reduced_domains		valid domains of the variables during the search;
							dictionary mapping variables to lists of values

		"""
		self.solutions = []
		self.csp = copy.deepcopy(csp) 
		self.reduced_domains = {var: list(self.csp.domains[var]) for var \
			in self.csp.vars}

	def get_delta_weight(self, assignment, var, val):
		""" Number multiplied by weight if we assign a new variable 
		assignment			partial assignment of variables;
							(dictionary mapping vars to assigned values)
		var					variable to be assigned, not yet in [assignment]
		val					value to be assigned to var
		"""
		assert (var not in assignment)
		assert (val in self.reduced_domains[var])
		delta = 1.0
		if self.csp.unary_factors[var] != None:
			delta = self.csp.unary_factors[var][val]
		for neighbor in self.csp.binary_factors[var]:
			if neighbor in assignment:
				assert (assignment[neighbor] in self.reduced_domains[neighbor])
				factor = self.csp.binary_factors[var][neighbor]
				delta *= factor[val][assignment[neighbor]]
				if delta == 0.0:
					return delta
		return delta

	def get_mcv_variable(self, assignment):
		""" Finds the most constrained variable to assign next
		assignment			partial assignment of variables;
							(dictionary mapping vars to assigned values)
		"""
		valid_vars = [var for var in self.csp.vars if var not in assignment]
		num_valid = [len([val for val in self.reduced_domains[var] \
			if self.get_delta_weight(assignment, var, val) != 0]) for var in valid_vars]
		num_valid_idx = [(num_valid[i], i) for i in range(len(valid_vars))]
		return valid_vars[min(num_valid_idx)[1]]
	
	def order_domain_by_lcv(self, var):
		""" Produces the domain of [var], with least constrained values first
		var				the variable to be assigned next
		"""
		neighbors = self.csp.binary_factors[var].keys()
		total_domains = {val: 0 for val in self.reduced_domains[var]}
		for val in total_domains:
			for neighbor in neighbors:
				factor = self.csp.binary_factors[var][neighbor]
				total_domains[val] += len([neigh_val for neigh_val \
					in self.reduced_domains[neighbor] if factor[val][neigh_val] > 0])
		return sorted(self.reduced_domains[var], key=lambda val: -total_domains[val])

	def arc_consistency_check(self, var):
		""" Executes the AC-3 algorithm for arc consistency (lookahead)
		var				the variable to be assigned next
		"""
		var_queue = [var]
		while len(var_queue) > 0:
			new_var = var_queue.pop(0)
			for neighbor in self.csp.binary_factors[new_var].keys():
				modified_domain = False
				to_remove = []
				for val in self.reduced_domains[neighbor]:
					if self.csp.unary_factors[neighbor] != None:
						if self.csp.unary_factors[neighbor][val] == 0:
							to_remove.append(val)
							modified_domain = True
							continue
					if self.csp.binary_factors[neighbor][new_var] != None:
						has_arc = False
						for new_val in self.reduced_domains[new_var]:
							if self.csp.binary_factors[neighbor][new_var][val][new_val] != 0:
								has_arc = True
						if not has_arc:
							to_remove.append(val)
							modified_domain = True
				for elem in to_remove:
					self.reduced_domains[neighbor].remove(elem)
				if modified_domain and neighbor not in var_queue:
					var_queue.append(neighbor)

	def backtrack(self, assignment, weight):
		""" Performs backtracking search, adding variables to [assignment]
		assignment			partial assignment of variables;
							(dictionary mapping vars to assigned values)
		weight				weight of the CSP, with the currently assigned vars
		"""
		assert (weight > 0)
		if len(assignment) == len(self.csp.vars):
			self.solutions.append((assignment.copy(), weight))
			return
		var = self.get_mcv_variable(assignment)
		values = self.order_domain_by_lcv(var)
		for val in values:
			delta_weight = self.get_delta_weight(assignment, var, val)
			if delta_weight > 0:
				assignment[var] = val
				orig_domains = copy.deepcopy(self.reduced_domains)
				self.reduced_domains[var] = [val]
				self.arc_consistency_check(var)
				self.backtrack(assignment, weight * delta_weight)
				self.reduced_domains = orig_domains
				del assignment[var]

	def solve(self):
		""" Solves the CSP, calling self.backtrack with an empty assignment
		"""
		self.solutions = []
		self.reduced_domains = {var: list(self.csp.domains[var]) for var \
			in self.csp.vars}
		self.backtrack({}, 1.0)

	def get_solutions(self):
		""" Orders the solutions by weight and returns the full assignments
		"""
		self.solutions = sorted(self.solutions, key=lambda sol: sol[0])
		return [assign for assign, weight in self.solutions]
