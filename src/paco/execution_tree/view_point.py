import math
from abc import ABC, abstractmethod

from paco.parser.tree_lib import CNode
from paco.saturate_execution.states import States, states_info


class ViewPoint(ABC):
	def __init__(self, id: int, states: States, decisions: tuple[CNode], is_final_state: bool, natures: tuple, choices:tuple, parent: 'ExecutionTree'):
		self.id = id
		self.states = states
		s, _ = self.states.str()
		self.state_id = s
		self.decisions = decisions
		self.is_final_state = is_final_state
		self.natures = natures
		self.choices = choices
		self.parent = parent
		self.transitions: dict[tuple, 'ExecutionTree'] = {}

	def __str__(self) -> str:
			return str(self.states)

	def __hash__(self):
		return hash(str(self))

	def add_child(self, subTree: 'ExecutionTree'):
		transition = []
		for i in range(len(subTree.root.decisions)):
			transition.append((subTree.root.decisions[i].parent,
							   subTree.root.decisions[i]))

		#for i in range(len(self.choices_natures)):
		#	transition.append((self.choices_natures[i], subTree.root.decisions[i],))

		self.transitions[tuple(transition)] = subTree


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

	def common_dot_str(self, full: bool = True, state: bool = True, executed_time: bool = False, previous_node: States = None):
		result = str(self).replace('(', '').replace(')', '').replace(';', '_').replace(':', '_').replace('-', "neg").replace(' | ', '_')

		if not full:
			return result

		result += f' [label=\"'

		s, d = self.states.str(previous_node)
		s = "Execution State:\n{" + s + "}"
		d = "Execution Time:\n{" + d + "}"

		label = f"ID: {self.id}\n"  # ""
		if state:
			label += s
		if state and executed_time:
			label += ",\n"
		if executed_time:
			label += d

		line_length = int(1.3 * math.sqrt(len(label)))
		return result + (self.text_format(label, line_length)) + "\", "

	@abstractmethod
	def dot_str(self, full: bool = True, state: bool = True, executed_time: bool = False, previous_node: States = None):
		pass

	@abstractmethod
	def dot_info_str(self):
		pass


def view_point_node_info(node: ViewPoint) -> str:
	result = f"ID:{node.id}:decisions:<"
	for n in list(node.decisions):
		result += str(n.id) + ";"
	result = result[:-1]

	if len(node.choices) > 0:
		result += ">:choices:<"
		tmp = ""
		for n in node.choices:
			tmp += str(n.id) + ";"
		result += tmp[:-1]
	if len(node.natures) > 0:
		result += ">:natures:<"
		tmp = ""
		for n in node.natures:
			tmp += str(n.id) + ";"
		result += tmp[:-1]

	return result + ">:status:\n" + states_info(node.states)

