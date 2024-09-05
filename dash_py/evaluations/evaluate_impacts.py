import copy
import numpy as np
from saturate_execution.states import States, ActivityState
from solver.tree_lib import CNode


def evaluate_expected_impacts(states: States, impacts_size: int):
	impacts = np.zeros(impacts_size, dtype=np.float64)
	probability = 1.0

	for node, state in states.activityState.items():
		if (node.type == 'natural' and state > ActivityState.WAITING
				and (states.activityState[node.childrens[0].root] > ActivityState.WAITING
					 or states.activityState[node.childrens[1].root] > ActivityState.WAITING)):

			p = node.probability
			if states.activityState[node.childrens[1].root] > 0:
				p = 1 - p
			probability *= p

		elif node.type == 'task' and state > ActivityState.WAITING:
			impacts += np.array(node.impact, dtype=np.float64)

	return probability, impacts


def unavoidable_tasks(root: CNode, states: States) -> set[CNode]:
	#print("root " + node_info(root, states))
	if root in states.activityState and states.activityState[root] in [ActivityState.WILL_NOT_BE_EXECUTED, ActivityState.COMPLETED, ActivityState.COMPLETED_WIHTOUT_PASSING_OVER]:
		#print("general node with: -1, 2, 3")
		return set()
	if root.type == 'task':
		if root not in states.activityState or (root in states.activityState and states.activityState[root] == ActivityState.WAITING):
			return set([root])
		return set()
	if root.type in ['sequential', 'parallel']:
		result = set[CNode]()
		for child in root.childrens:
			result = result.union(unavoidable_tasks(child.root, states))
		return result

	if root.type in ['choice', 'natural'] and root in states.activityState and states.activityState[root] == ActivityState.ACTIVE:
		for child in root.childrens:
			if child.root in states.activityState and states.activityState[child.root] == ActivityState.ACTIVE:
				return unavoidable_tasks(child.root, states)

	return set()


def evaluate_unavoidable_impacts(root: CNode, states: States, current_impacts: np.array) -> np.array:
	unavoidableImpacts = copy.deepcopy(current_impacts)
	#print("Unavoidable:\n" + states_info(states))
	for unavoidableTask in unavoidable_tasks(root, states):
		#print("unavoidableTask: " + node_info(unavoidableTask, states))
		unavoidableImpacts += np.array(unavoidableTask.impact)

	return unavoidableImpacts
