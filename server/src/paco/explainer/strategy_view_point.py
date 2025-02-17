import numpy as np

from paco.execution_tree.execution_tree import ExecutionTree
from paco.execution_tree.view_point import ViewPoint
from paco.explainer.bdd.bdd import Bdd
from paco.parser.tree_lib import CNode
from paco.saturate_execution.states import States


class StrategyViewPoint(ViewPoint):
	def __init__(self, bpmn_root: CNode, id: int, states: States, decisions: tuple[CNode], choices: dict[CNode:Bdd], natures: list[CNode],
				 is_final_state: bool, probability:float, impacts: np.ndarray, parent: ExecutionTree = None):
		super().__init__(id, states, decisions, is_final_state, tuple(natures), tuple(choices), parent)

		# Each choice is a key and the value is the bdd (None if arbitrary)
		self.explained_choices: dict[CNode:Bdd] = {choice: None for choice in choices}
		# initially all choices are arbitrary, will be updated using make_decisions

		self.probability = probability
		self.impacts = impacts
		self.executed_time = states.executed_time[bpmn_root]
		self.expected_impacts = probability * impacts
		self.expected_time = probability * self.executed_time

	def dot_str(self, full: bool = True, state: bool = True, executed_time: bool = False, previous_node: States = None):
		result = super().common_dot_str(full, state, executed_time, previous_node)
		if full:
			#print(f"ID: {self.id}, choice: ", len(self.choices), "natures: ", len(self.natures))
			choices_number = len(self.explained_choices)
			natures_number = len(self.natures)
			if choices_number > 0 and natures_number == 0:
				result += "style=filled, fillcolor=\"orange\""
			elif choices_number == 0 and natures_number > 0:
				result += "style=filled, fillcolor=\"yellowgreen\""
			elif choices_number > 0 and natures_number > 0:
				result += "style=wedged, fillcolor=\"yellowgreen;0.5:orange\""

			result += "];\n"

		return result

	def dot_info_str(self):
		label = f" [label=\""
		label += f"Time: {self.executed_time}\n"
		label += f"Impacts: {self.impacts}\n"
		if self.probability != 1:
			label += f"Probability: {round(self.probability, 2)}\n"
			label += f"Exp. Time: {round(self.expected_time, 2)}\n"
			label += f"Exp. Impacts: {np.round(self.expected_impacts, 2)}\n"
		if len(self.natures) > 0:
			label += "Nature: "
			for nature in list(self.natures):
				label += f"{nature.name}, "
			label = label[:-2] + "\n"
		if len(self.explained_choices) > 0:
			label += "Choice:\n"
			for choice, bdd in self.explained_choices.items():
				label += f"{choice.name}: {'arbitrary' if bdd is None else str(bdd.typeStrategy)}\n"

		label += "\", shape=rect];\n"
		return (self.dot_str(full=False) + "_impact", label)
