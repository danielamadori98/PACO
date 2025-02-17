import copy
import enum
import numpy as np
from paco.parser.tree_lib import CNode, CTree
from paco.execution_tree.execution_tree import ExecutionTree
from paco.evaluations.evaluate_decisions import evaluate_decisions, find_all_decisions
from paco.evaluations.evaluate_impacts import evaluate_unavoidable_impacts


class ExplanationType(enum.IntEnum):
	CURRENT_IMPACTS = 0
	UNAVOIDABLE_IMPACTS = 1
	DECISION_BASED = 2
	HYBRID = 3

	def __str__(self):
		return str(self.name)


def current_impacts(decisions: dict[CNode, set[ExecutionTree]]) -> (list, list):
	#print("Current impacts:")
	impacts, impacts_labels = [], []
	for decision_taken, executionTrees in decisions.items():
		#print(f"Decision: {decision_taken.name if decision_taken.name else decision_taken.id} has {len(executionTrees)} execution trees")
		for executionTree in executionTrees:
			#print(f"I({decision_taken.name if decision_taken.name else decision_taken.id}): {executionTree.root.impacts}")
			impacts.append(copy.deepcopy(executionTree.root.impacts))
			impacts_labels.append(decision_taken.id)

	return impacts, impacts_labels


def unavoidable_impacts(region_tree: CTree, decisions: dict[CNode, set[ExecutionTree]]) -> (list, list):
	#print("Unavoidable impacts:")
	impacts, impacts_labels = [], []
	for decision_taken, executionTrees in decisions.items():
		#print(f"Decision: {decision_taken.name if decision_taken.name else decision_taken.id} has {len(executionTrees)} execution trees")
		for executionTree in executionTrees:
			impacts.append(
				evaluate_unavoidable_impacts(region_tree.root,
											 executionTree.root.states,
											 executionTree.root.impacts)
			)
			impacts_labels.append(decision_taken.id)
			#print(f"UI({decision_taken.name if decision_taken.name else decision_taken.id}): {impacts[-1]}")

	return impacts, impacts_labels


def decision_based(region_tree: CTree, decisions_taken: dict[CNode, set[ExecutionTree]]) -> (list[CNode], list[np.ndarray], list):
	decisions, decisions_names = find_all_decisions(region_tree)
	decision_vectors, labels = [], []
	#print(f"Decision based:\n{decisions_names}")
	for decision_taken, executionTrees in decisions_taken.items():
		#print(f"Decision: {decision_taken.name if decision_taken.name else decision_taken.id} has {len(executionTrees)} execution trees")
		for executionTree in executionTrees:
			decision_vectors.append(evaluate_decisions(decisions, executionTree.root.states.activityState))
			labels.append(decision_taken.id)
			#print(f"DB({decision_taken.name if decision_taken.name else decision_taken.id}): {decision_vectors[-1]}")

	return decisions_names, decision_vectors, labels
