import copy
import math
import os
import numpy as np
import pydot
from graphviz import Source
from solver.tree_lib import CNode, CTree
from saturate_execution.saturate_execution import saturate_execution
from saturate_execution.states import States, states_info, ActivityState
from utils.env import PATH_EXECUTION_TREE, RESOLUTION, PATH_AUTOMA_STATE_DOT, PATH_AUTOMA_STATE_IMAGE_SVG, \
	PATH_AUTOMA_STATE_TIME_DOT, \
	PATH_AUTOMA_TIME_IMAGE_SVG, PATH_AUTOMA_STATE_TIME_EXTENDED_DOT, \
	PATH_AUTOMA_STATE_TIME_EXTENDED_IMAGE_SVG, PATH_AUTOMA_TIME_DOT


class ExecutionViewPoint:
	def __init__(self, id: int, states: States, decisions: tuple[CNode], choices_natures: tuple,
				 is_final_state: bool, impacts_names, parent: 'ExecutionTree' = None):
		self.id = id
		self.states = states
		s, _ = self.states.str()
		self.state_id = s
		self.decisions = decisions
		self.choices_natures = choices_natures
		self.parent = parent
		self.is_final_state = is_final_state
		self.transitions: dict[tuple, ExecutionTree] = {}
		self.expected_impacts_evaluation(len(impacts_names))
		self.cei_bottom_up = np.zeros(len(impacts_names), dtype=np.float64)

	def __str__(self) -> str:
		return str(self.states)

	def __hash__(self):
		return hash(str(self))

	@staticmethod
	def text_format(text: str, line_length: int):
		parts = []
		current_part = ""
		char_count = 0

		for char in text:
			current_part += char
			char_count += 1
			if char == ';' and char_count >= line_length:
				parts.append(current_part)
				current_part = ""
				char_count = 0

		if current_part:
			parts.append(current_part)

		return "\\n".join(parts)

	def dot_str(self, full: bool = True, state: bool = True, executed_time: bool = False, previous_node: States = None):
		result = str(self).replace('(', '').replace(')', '').replace(';', '_').replace(':', '_').replace('-',
																										 "neg").replace(
			' | ', '_')

		if full:
			result += f' [label=\"'

			s, d = self.states.str(previous_node)
			s = "q|s:{" + s + "}"
			d = "q|delta:{" + d + "}"

			label = f"ID: {self.id}\n" # ""
			if state:
				label += s
			if state and executed_time:
				label += ",\n"
			if executed_time:
				label += d

			line_length = int(1.3 * math.sqrt(len(label)))
			result += self.text_format(label, line_length) + "\"];\n"

		return result

	def add_child(self, subTree: 'ExecutionTree'):
		transition = []
		for i in range(len(self.choices_natures)):
			transition.append((self.choices_natures[i], subTree.root.decisions[i],))

		self.transitions[tuple(transition)] = subTree


	# Is just an idea, doesn't work it might add the same impact twice
	# TODO: Fix this
	def get_expected_impacts_evaluation_from_region_tree(self, region_tree: CTree):
		root = region_tree.root

		if root not in self.states.activityState:
			return

		state = self.states.activityState[root]

		if root.type == 'task' and state > ActivityState.WAITING:
			self.impacts += np.array(root.impact, dtype=np.float64)
			return

		if (root.type == 'natural' and state > ActivityState.WAITING
				and (self.states.activityState[root.childrens[0].root] > ActivityState.WAITING
					 or self.states.activityState[root.childrens[1].root] > ActivityState.WAITING)):

			p = root.probability
			if self.states.activityState[root.childrens[1].root] > 0:
				p = 1 - p
			self.probability *= p

		for sub_region in root.childrens:
			self.get_expected_impacts_evaluation_from_region_tree(sub_region)


	def expected_impacts_evaluation(self, impacts_size: int):
		if self.parent is None: # Root execution view point
			self.probability = 1.0
			self.impacts = np.zeros(impacts_size, dtype=np.float64)
			self.get_expected_impacts_evaluation_from_region_tree(CTree(self.decisions[0])) #Provide the region tree of the root CNode
		else:
			self.probability = self.parent.probability
			self.impacts = copy.deepcopy(self.parent.impacts)
			for choice_nature in self.choices_natures:
				self.get_expected_impacts_evaluation_from_region_tree(CTree(choice_nature))

		self.cei_top_down = self.probability * self.impacts


	def dot_cei_str(self):
		return (self.dot_str(full=False) + "_impact",
				f" [label=\"(cei_td: {self.cei_top_down},\ncei_bu: {self.cei_bottom_up})\", shape=rect];\n")
				#f" [label=\"ID: {self.id} (cei_td: {self.cei_top_down},\ncei_bu: {self.cei_bottom_up})\", shape=rect];\n")


class ExecutionTree:
	def __init__(self, root: ExecutionViewPoint):
		self.root = root

	def __str__(self) -> str:
		result = self.create_dot_graph(self.root, True, True, False)
		return result[0] + result[1]

	def state_str(self):
		return self.root.dot_str(state=True, executed_time=True, previous_node=None).split(' [')[0]

	def save_dot(self, path, state: bool = True, executed_time: bool = False, diff: bool = True):
		with open(path, 'w') as file:
			file.write(self.init_dot_graph(state=state, executed_time=executed_time, diff=diff))

	def save_pdf(self, path, state: bool = True, executed_time: bool = False, diff: bool = True):
		Source(self.init_dot_graph(state=state, executed_time=executed_time, diff=diff),
			   format='pdf').render(path, cleanup=True)

	def init_dot_graph(self, state: bool, executed_time: bool, diff: bool):
		result = "digraph automa {\n"

		node, transition = self.create_dot_graph(self.root, state=state, executed_time=executed_time,
												 diff=diff)

		result += node
		result += transition
		result += "__start0 [label=\"\", shape=none];\n"

		starting_node_ids = ""
		for n in self.root.decisions:
			starting_node_ids += str(n.id) + ";"

		if len(self.root.choices_natures) > 0:  #Just if we don't have choice
			starting_node_ids = starting_node_ids[:-1] + "->"
			for n in self.root.choices_natures:
				starting_node_ids += str(n.id) + ";"

		result += f"__start0 -> {self.root.dot_str(full=False)}  [label=\"{starting_node_ids[:-1]}\"];\n" + "}"
		return result

	def create_dot_graph(self, root: ExecutionViewPoint, state: bool, executed_time: bool, diff: bool,
						 previous_node: States = None):
		if diff == False:# print all nodes
			previous_node = None

		nodes_id = root.dot_str(state=state, executed_time=executed_time, previous_node=previous_node)
		transitions_id = ""

		impact_id, impact_label = root.dot_cei_str()
		transitions_id += f"{root.dot_str(full=False)} -> {impact_id} [label=\"\" color=red];\n"  #style=invis
		nodes_id += impact_id + impact_label

		for transition in root.transitions.keys():
			next_node = root.transitions[transition].root
			x = ""
			for t in transition:
				x += str(t[0].id) + '->' + str(t[1].id) + ';'
			#x += str(t)[1:-1].replace(',', '->') + ";"

			transitions_id += f"{root.dot_str(full=False)} -> {next_node.dot_str(full=False)} [label=\"{x[:-1]}\"];\n"

			ids = self.create_dot_graph(next_node, state=state, executed_time=executed_time, diff=diff,
										previous_node=root.states)
			nodes_id += ids[0]
			transitions_id += ids[1]

		return nodes_id, transitions_id


def tree_node_info(node: ExecutionViewPoint) -> str:
	result = f"ID:{node.id}:decisions:<"
	for n in node.decisions:
		result += str(n.id) + ";"
	result = result[:-1]

	if len(node.choices_natures) > 0:
		result += ">:choices_natures:<"
		tmp = ""
		for n in node.choices_natures:
			tmp += str(n.id) + ";"
		result += tmp[:-1]

	return result + ">:status:\n" + states_info(node.states)


def create_execution_tree(region_tree: CTree, impacts_names:list) -> (ExecutionTree, list[ExecutionTree]):
	states, choices_natures, branches = saturate_execution(region_tree, States(region_tree.root, ActivityState.WAITING, 0))

	id = 0
	solution_tree = ExecutionTree(ExecutionViewPoint(
		id=id, states=states,
		decisions=(region_tree.root,),
		choices_natures=choices_natures,
		is_final_state=states.activityState[region_tree.root] >= ActivityState.COMPLETED,
		impacts_names=impacts_names)
	)

	print("create_tree:", tree_node_info(solution_tree.root))

	for decisions, branch_states in branches.items():
		branch = copy.deepcopy(states)
		branch.update(branch_states)
		id = create_execution_viewpoint(region_tree, decisions, branch, solution_tree, id + 1, impacts_names)

	return solution_tree


def create_execution_viewpoint(region_tree: CTree, decisions: tuple[CNode], states: States, solution_tree: ExecutionTree, id: int, impacts_names:list) -> (list, int):
	saturatedStates, choices_natures, branches = saturate_execution(region_tree, states)
	states.update(saturatedStates)

	next_node = ExecutionTree(ExecutionViewPoint(
		id=id,
		states=states,
		decisions=decisions,
		choices_natures=choices_natures,
		is_final_state=states.activityState[region_tree.root] >= ActivityState.COMPLETED,
		impacts_names=impacts_names,
		parent=solution_tree)
	)

	print("create_tree_node:", tree_node_info(next_node.root))

	solution_tree.root.add_child(next_node)
	for decisions, branch_states in branches.items():
		branch = copy.deepcopy(states)
		branch.update(branch_states)
		id = create_execution_viewpoint(region_tree, decisions, branch, next_node, id + 1, impacts_names)
	return id


def write_image(frontier: list[ExecutionTree], dotPath: str, svgPath: str = "", pngPath: str = ""):
	graphs = pydot.graph_from_dot_file(dotPath)
	graph = graphs[0]
	# print([node.get_name() for node in graph.get_nodes()])
	# color the winning nodes
	if frontier is not None:
		for el in frontier:
			node = graph.get_node('"' + el.state_str() + '"')[0]
			node.set_style('filled')
			node.set_fillcolor('green')

	# if svgPath not ""
	if svgPath != "":
		graph.write_svg(svgPath)

	graph.set('dpi', RESOLUTION)
	if pngPath != "":
		graph.write_png(pngPath)


def write_execution_tree(solution_tree: ExecutionTree, frontier: list[ExecutionTree] = []):
	if not os.path.exists(PATH_EXECUTION_TREE):
		os.makedirs(PATH_EXECUTION_TREE)
	solution_tree.save_dot(PATH_AUTOMA_STATE_DOT)
	write_image(frontier, PATH_AUTOMA_STATE_DOT, svgPath=PATH_AUTOMA_STATE_IMAGE_SVG)#, PATH_AUTOMA_IMAGE)

	solution_tree.save_dot(PATH_AUTOMA_STATE_TIME_DOT, executed_time=True)
	write_image(frontier, PATH_AUTOMA_STATE_TIME_DOT, svgPath=PATH_AUTOMA_TIME_IMAGE_SVG)#, PATH_AUTOMA_TIME_IMAGE)

	solution_tree.save_dot(PATH_AUTOMA_STATE_TIME_EXTENDED_DOT, executed_time=True, diff=False)
	write_image(frontier, PATH_AUTOMA_STATE_TIME_EXTENDED_DOT, svgPath=PATH_AUTOMA_STATE_TIME_EXTENDED_IMAGE_SVG)#, PATH_AUTOMA_TIME_EXTENDED_IMAGE)

	solution_tree.save_dot(PATH_AUTOMA_TIME_DOT, state=False, executed_time=True)
	write_image(frontier, PATH_AUTOMA_TIME_DOT, svgPath=PATH_AUTOMA_TIME_IMAGE_SVG)#, PATH_AUTOMA_TIME_IMAGE)





