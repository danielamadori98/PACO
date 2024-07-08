import re
import copy
from solver.tree_lib import CTree
from solver.automaton_graph import AGraph, ANode
from solver_optimized.create_automa_state import create_automa_state
from solver_optimized.states import States, states_info, ActivityState


def create_automa(region_tree: CTree) -> AGraph:
	branches, states = create_automa_state(region_tree, States(region_tree.root, ActivityState.WAITING, 0))

	current_node_id = re.sub(r':[^;]*;', ';', list(branches.keys())[0])# Get id of the first choice/nature node
	print("create_automa:root:" + current_node_id + states_info(states))

	automa = AGraph(ANode(
		states=states,
		process_ids=current_node_id,
		is_final_state=states.activityState[region_tree.root] >= ActivityState.COMPLETED)
	)

	final_states = []
	for next_node_id in branches.keys():
		branch = copy.deepcopy(states)
		branch.update(branches[next_node_id])
		print(f"create_automa:next_node_id:{next_node_id}:\n" + states_info(branch))
		final_states.extend(
			create_next_automa_state(region_tree, branch, automa, next_node_id)
		)

	return automa, final_states


def create_next_automa_state(region_tree: CTree, states: States, automa: AGraph, transitions: str):
	branches, updatedStates = create_automa_state(region_tree, states)
	print("create_next_automa_state:states:" + states_info(states))

	states.update(updatedStates)
	is_final_state = states.activityState[region_tree.root] >= ActivityState.COMPLETED
	final_states = []
	next_node = AGraph(ANode(
		states=states,
		process_ids=transitions,
		is_final_state=is_final_state)
	)
	if is_final_state:
		final_states.append(next_node)

	automa.init_node.add_transition(next_node)

	for next_transitions in branches.keys():
		branch = copy.deepcopy(states)
		branch.update(branches[next_transitions])
		print("create_automa:next_node_id:" + next_transitions + states_info(branch))
		final_states.extend(
			create_next_automa_state(region_tree, branch, next_node, next_transitions)
		)

	return final_states