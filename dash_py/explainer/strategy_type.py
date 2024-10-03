import copy
import enum

from evaluations.evaluate_execution_path import evaluate_execution_path
from evaluations.evaluate_impacts import evaluate_unavoidable_impacts
from parser.tree_lib import CNode, CTree
from solver.execution_tree import ExecutionTree

class TypeStrategy(enum.IntEnum):
	CURRENT_IMPACTS = 0
	UNAVOIDABLE_IMPACTS = 1
	DECISION_BASED = 2

	def __str__(self):
		return str(self.value)


def current_impacts(decisions: dict[CNode, set[ExecutionTree]]) -> (list, list):
	impacts, impacts_labels = [], []
	for decision, executionTrees in decisions.items():
		print(f"Decision: {decision.id} has {len(executionTrees)} execution trees")
		for executionTree in executionTrees:
			impacts.append(copy.deepcopy(executionTree.root.impacts))
			impacts_labels.append(decision.id)

	return impacts, impacts_labels

def unavoidable_impacts(region_tree: CTree, decisions: dict[CNode, set[ExecutionTree]]) -> (list, list):
	impacts, impacts_labels = [], []
	for decision, executionTrees in decisions.items():
		for executionTree in executionTrees:
			impacts.append(
				evaluate_unavoidable_impacts(region_tree.root,
											 executionTree.root.states,
											 executionTree.root.impacts)
			)
			impacts_labels.append(decision.id)

	return impacts, impacts_labels

def decision_based(decisions: dict[CNode, set[ExecutionTree]]):
	decision_vectors, labels = [], []
	for decision, executionTrees in decisions.items():
		for executionTree in executionTrees:
			decision_vectors.append(executionTree.root.states.activityState)
			labels.append(decision.id)

	all_nodes, decision_vectors = evaluate_execution_path(decision_vectors)
	
	s = ''
	for node in all_nodes:
		s += str(node.id) + ', '
	print("\t\t  ID: ", s [:-2])
	for i in range(len(decision_vectors)):
		print(f"Decision vector: {decision_vectors[i]}, label: {labels[i]}")

	return all_nodes, decision_vectors, labels
