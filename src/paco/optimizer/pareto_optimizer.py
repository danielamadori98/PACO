import numpy as np
import random
from paco.optimizer.pareto import get_min_dominated_impacts, get_max_dominating_vectors, get_dominated_vectors
from paco.searcher.found_strategy import compare_bound
from paco.solver import paco
from utils.env import IMPACTS_NAMES


def pareto_optimal_impacts(bpmn: dict, max_bound:np.ndarray= None, decimal_number: int = 0):
	parse_tree = None
	execution_tree = None
	min_solutions = []
	possible_min_solution = []
	if max_bound is None:
		possible_min_solution.append(np.zeros(len(bpmn[IMPACTS_NAMES]), dtype=np.float64))
	else:
		possible_min_solution.append(max_bound)

	i = 0
	found_optimal = False
	bound = np.zeros(len(bpmn[IMPACTS_NAMES]), dtype=np.float64)
	while True:
		s = ""
		for j in range(len(min_solutions)):
			s += f"Impacts {j}:\t{min_solutions[j]}\n"
		#print(f"Guaranteed Bound:\n", s)

		s = ""
		for j in range(len(possible_min_solution)):
			s += f"Impacts {j}:\t{possible_min_solution[j]}\n"
		#print(f"Possible Bound:\n", s)

		solutions = []
		if max_bound is not None:
			solutions = [solution for solution in min_solutions if np.all(compare_bound(solution, max_bound) <= 0)]

		if len(possible_min_solution) == 0 or len(solutions) > 0:
			found_optimal = True

			if len(solutions) > 0:
				print("Max bound found")
				bound = solutions.pop(random.randint(0, len(solutions)-1))

			if len(min_solutions) > 0:
				print("Min solutions found")
				bound = min_solutions.pop(random.randint(0, len(min_solutions)-1))

		else:
			bound = possible_min_solution.pop(random.randint(0, len(possible_min_solution)-1))

		print(f"Attempt {i}:\t{bpmn[IMPACTS_NAMES]}\nSelected:\t{bound}\n")

		text_result, parse_tree, execution_tree, expected_impacts, new_possible_min_solution, new_min_solutions, choices, name_svg = paco(bpmn, bound, parse_tree, execution_tree, search_only=not found_optimal)

		if found_optimal:
			print("Optimal solution found")
			break

		#a: Finds the vectors in new_possible_min_solution dominated by vectors in new_min_solutions.
		#b: Finds the vectors in new_min_solutions dominated by vectors in new_possible_min_solution.
		a, b = get_dominated_vectors(new_possible_min_solution, new_min_solutions)
		if len(b) > 0:
			print("Limit found")
			for ei in b:
				print("Limit:", ei)
		else:
			possible_min_solution.extend([np.round(ei, decimal_number) for ei in new_possible_min_solution])
			min_solutions.extend([np.round(ei, decimal_number) for ei in new_min_solutions])
			if expected_impacts is not None:
				min_solutions.append(expected_impacts)

		possible_min_solution = get_max_dominating_vectors(possible_min_solution)
		min_solutions = get_min_dominated_impacts(min_solutions)

		i += 1

	return bound, expected_impacts, min_solutions, parse_tree, execution_tree, choices
