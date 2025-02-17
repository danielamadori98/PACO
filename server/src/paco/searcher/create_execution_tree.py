import copy
import os
import pydot

from paco.execution_tree.execution_view_point import ExecutionViewPoint
from paco.parser.tree_lib import CNode, CTree
from paco.saturate_execution.saturate_execution import saturate_execution_decisions
from paco.saturate_execution.states import States, ActivityState
from paco.execution_tree.execution_tree import ExecutionTree
from utils.env import PATH_EXECUTION_TREE, RESOLUTION, PATH_AUTOMA_STATE_DOT, PATH_AUTOMA_STATE_IMAGE_SVG, \
	PATH_AUTOMA_STATE_TIME_DOT, \
	PATH_AUTOMA_TIME_IMAGE_SVG, PATH_AUTOMA_STATE_TIME_EXTENDED_DOT, \
	PATH_AUTOMA_STATE_TIME_EXTENDED_IMAGE_SVG, PATH_AUTOMA_TIME_DOT


def create_execution_tree(region_tree: CTree, impacts_names:list) -> (ExecutionTree, list[ExecutionTree]):
	states, choices, natures, branches = saturate_execution_decisions(region_tree, States(region_tree.root, ActivityState.WAITING, 0))

	id = 0
	solution_tree = ExecutionTree(ExecutionViewPoint(
		id=id, states=states,
		decisions=(region_tree.root,),
		choices=choices, natures=natures,
		is_final_state=states.activityState[region_tree.root] >= ActivityState.COMPLETED,
		impacts_names=impacts_names)
	)

	#print("create_execution_tree:", tree_node_info(solution_tree.root))

	for decisions, branch_states in branches.items():
		branch = copy.deepcopy(states)
		branch.update(branch_states)
		id = create_execution_viewpoint(region_tree, decisions, branch, solution_tree, id + 1, impacts_names)

	return solution_tree


def create_execution_viewpoint(region_tree: CTree, decisions: tuple[CNode], states: States, solution_tree: ExecutionTree, id: int, impacts_names:list) -> int:
	saturatedStates, choices, natures, branches = saturate_execution_decisions(region_tree, states)
	states.update(saturatedStates)

	next_node = ExecutionTree(ExecutionViewPoint(
		id=id,
		states=states,
		decisions=decisions,
		choices=choices, natures=natures,
		is_final_state=states.activityState[region_tree.root] >= ActivityState.COMPLETED,
		impacts_names=impacts_names,
		parent=solution_tree)
	)

	#print("create_execution_viewpoint:", tree_node_info(next_node.root))

	solution_tree.root.add_child(next_node)
	for decisions, branch_states in branches.items():
		branch = copy.deepcopy(states)
		branch.update(branch_states)
		id = create_execution_viewpoint(region_tree, decisions, branch, next_node, id + 1, impacts_names)
	return id


def write_image(frontier: list[ExecutionTree], dotPath: str, svgPath: str = "", pngPath: str = ""):
	graphs = pydot.graph_from_dot_file(dotPath)
	graph = graphs[0]

	for e in frontier:
		node = graph.get_node('"' + e.state_str() + '"')[0]
		node.set_style('filled')
		node.set_fillcolor('lightblue')

	if svgPath != "":
		graph.write_svg(svgPath)

	graph.set('dpi', RESOLUTION)
	if pngPath != "":
		graph.write_png(pngPath)


def write_execution_tree(solution_tree: ExecutionTree, frontier: list[ExecutionTree] = []):
	if not os.path.exists(PATH_EXECUTION_TREE):
		os.makedirs(PATH_EXECUTION_TREE)
	solution_tree.save_dot(PATH_AUTOMA_STATE_DOT, diff=False)
	write_image(frontier, PATH_AUTOMA_STATE_DOT, svgPath=PATH_AUTOMA_STATE_IMAGE_SVG)#, PATH_AUTOMA_IMAGE)

	solution_tree.save_dot(PATH_AUTOMA_STATE_TIME_DOT, executed_time=True)
	write_image(frontier, PATH_AUTOMA_STATE_TIME_DOT, svgPath=PATH_AUTOMA_TIME_IMAGE_SVG)#, PATH_AUTOMA_TIME_IMAGE)

	solution_tree.save_dot(PATH_AUTOMA_STATE_TIME_EXTENDED_DOT, executed_time=True, diff=False)
	write_image(frontier, PATH_AUTOMA_STATE_TIME_EXTENDED_DOT, svgPath=PATH_AUTOMA_STATE_TIME_EXTENDED_IMAGE_SVG)#, PATH_AUTOMA_TIME_EXTENDED_IMAGE)

	solution_tree.save_dot(PATH_AUTOMA_TIME_DOT, state=False, executed_time=True)
	write_image(frontier, PATH_AUTOMA_TIME_DOT, svgPath=PATH_AUTOMA_TIME_IMAGE_SVG)#, PATH_AUTOMA_TIME_IMAGE)

	os.remove(PATH_AUTOMA_STATE_DOT)
	os.remove(PATH_AUTOMA_STATE_TIME_DOT)
	os.remove(PATH_AUTOMA_TIME_DOT)
	os.remove(PATH_AUTOMA_STATE_TIME_EXTENDED_DOT)
