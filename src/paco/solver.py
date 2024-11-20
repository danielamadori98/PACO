import numpy as np
from paco.explainer.build_explained_strategy import build_explained_strategy
from paco.explainer.explanation_type import ExplanationType
from paco.parser.create import create
from paco.searcher.search import search
from utils import check_syntax as cs
from utils.env import IMPACTS_NAMES, DURATIONS, PATH_IMAGE_BPMN
from datetime import datetime
from paco.parser.print_sese_diagram import print_sese_diagram


def paco(bpmn:dict, bound:np.ndarray, parse_tree=None, execution_tree=None, search_only=False, type_strategy=ExplanationType.HYBRID):
	#print(f'{datetime.now()} Testing PACO...')
	print(f'{datetime.now()} Bound {bound}')

	#print(f'{datetime.now()} bpmn + cpi {bpmn}')
	if parse_tree is None or execution_tree is None:
		print_sese_diagram(**bpmn, outfile=PATH_IMAGE_BPMN)
		bpmn[DURATIONS] = cs.set_max_duration(bpmn[DURATIONS]) # set max duration
		parse_tree, execution_tree = create(bpmn)

	expected_impacts, possible_min_solution, solutions, strategy = search(execution_tree, bound, bpmn[IMPACTS_NAMES], search_only)

	if expected_impacts is None:
		text_result = ""
		for i in range(len(possible_min_solution)):
			text_result += f"Exp. Impacts {i}:\t{np.round(possible_min_solution[i], 2)}\n"
		print(f"Failed:\t\t\t{bpmn[IMPACTS_NAMES]}\nPossible Bound Impacts:\t{bound}\n" + text_result)
		text_result = ""
		for i in range(len(solutions)):
			text_result += f"Guaranteed Bound {i}:\t{np.ceil(solutions[i])}\n"

		print(str(datetime.now()) + " " + text_result)
		return text_result, parse_tree, execution_tree, expected_impacts, possible_min_solution, solutions, []

	if strategy is None:
		text_result = f"Any choice taken will provide a winning strategy with an expected impact of: "
		text_result += " ".join(f"{key}: {round(value,2)}" for key, value in zip(bpmn[IMPACTS_NAMES],  [item for item in expected_impacts]))
		print(str(datetime.now()) + " " + text_result)
		return text_result, parse_tree, execution_tree, expected_impacts, possible_min_solution, solutions, []

	strategy_tree, expected_impacts, strategy_expected_time, choices = build_explained_strategy(parse_tree, strategy, type_strategy, bpmn[IMPACTS_NAMES])

	text_result = f"This is the strategy, with an expected impact of: "
	text_result += " ".join(f"{key}: {round(value,2)}" for key, value in zip(bpmn[IMPACTS_NAMES],  [item for item in expected_impacts]))

	#TODO Return strategy tree if found
	print(str(datetime.now()) + " " + text_result)
	return text_result, parse_tree, execution_tree, expected_impacts, possible_min_solution, solutions, choices
