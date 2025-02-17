from paco.parser.tree_lib import CNode
from paco.saturate_execution.states import States, ActivityState
from itertools import product


def create_branches(states: States) -> (tuple[CNode], dict[tuple[CNode], States]):
	choices_natures = []
	choices = []
	natures = []
	node: CNode
	for node in list(states.activityState.keys()):
		if ((node.type == 'choice' or node.type == 'natural')
				and states.activityState[node] == ActivityState.ACTIVE
				and states.executed_time[node] == node.max_delay
				and states.activityState[node.children[0].root] == ActivityState.WAITING
				and states.activityState[node.children[1].root] == ActivityState.WAITING):

			if node.type == 'choice':
				choices.append(node)
			else:
				natures.append(node)

			choices_natures.append(node)
			#print(f"create_branches:active_choice-nature:" + node_info(node, states))

	branches = {}
	if len(choices_natures) == 0:
		return tuple(choices), tuple(natures), branches

	branches_choices = list(product([True, False], repeat=len(choices_natures)))
	#print(f"create_branches:cardinality:{choice_nature_dim}:combinations:{branches_choices}")
	for branch_choices in branches_choices:
		branch_states = States() # Original code: branch_states = copy.deepcopy(states)
		decisions = []
		for i in range(len(choices_natures)):
			node = choices_natures[i]

			if branch_choices[i]:
				activeNode = node.children[0].root
				inactiveNode = node.children[1].root
			else:
				activeNode = node.children[1].root
				inactiveNode = node.children[0].root

			decisions.append(activeNode)
			branch_states.activityState[activeNode] = ActivityState.ACTIVE
			branch_states.activityState[inactiveNode] = ActivityState.WILL_NOT_BE_EXECUTED

		branches[tuple(decisions)] = branch_states

	return tuple(choices), tuple(natures), branches
