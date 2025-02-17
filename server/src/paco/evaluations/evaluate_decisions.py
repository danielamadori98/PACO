import numpy as np
from paco.saturate_execution.states import ActivityState
from paco.parser.tree_lib import CNode, CTree


def find_all_decisions_rec(tree: CTree) -> list[CNode]:
	if not tree.root.children:
		return []

	decisions = [child.root for child in tree.root.children if tree.root.type in {'choice', 'natural'}]
	for subTree in tree.root.children:
		decisions.extend(find_all_decisions_rec(subTree))

	return decisions


def find_all_decisions(region_tree: CTree) -> (list[CNode], list[str]):
	decisions = sorted(find_all_decisions_rec(region_tree), key=lambda d: d.id)
	decisions_names = [f"{d.parent.name}_{'0' if d.parent.children[0].root == d else '1'}" for d in decisions]
	return decisions, decisions_names


def evaluate_decisions(decisions: list[CNode], execution: ActivityState) -> np.ndarray:
	return np.array([0 if decision not in execution or execution[decision] < ActivityState.ACTIVE
					 else 1 for decision in decisions], dtype='int')
