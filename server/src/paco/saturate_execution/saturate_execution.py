from paco.parser.tree_lib import CTree, CNode
from paco.saturate_execution.create_branches import create_branches
from paco.saturate_execution.next_state import next_state
from paco.saturate_execution.states import States, ActivityState
from paco.saturate_execution.step_to_saturation import steps_to_saturation

# Saturation of the execution tree activating decisions nodes
def saturate_execution_decisions(region_tree: CTree, states: States) -> (States, tuple[CNode], dict[tuple[CNode], States]):
	branches = dict()
	choices = tuple()
	natures = tuple()

	while len(choices) + len(natures) == 0 and states.activityState[region_tree.root] < ActivityState.COMPLETED:
		#print("step_to_saturation:")
		#print("start:", states_info(states))

		k = steps_to_saturation(region_tree, states)
		#print('step_to_saturation:k:', k, states_info(states))

		updatedStates, k = next_state(region_tree, states, k)
		states.update(updatedStates)

		#print('next_state:k:', k, states_info(states))
		if k > 0:
			raise Exception("saturate_execution:StepsException" + str(k))

		choices, natures, branches = create_branches(states)

	#if len(branches) > 0:
		#print("create_branches:", states_info(states))

	#print("Branches:" + str(len(branches)))
	#print("Root activity state: ", states.activityState[region_tree.root], states_info(states))

	return states, choices, natures, branches
