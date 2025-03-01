import numpy as np

from paco.evaluations.evaluate_impacts import evaluate_expected_impacts
from paco.parser.parse_node import ParseNode
from paco.saturate_execution.states import States
from paco.execution_tree.view_point import ViewPoint


class ExecutionViewPoint(ViewPoint):
	def __init__(self, id: int, states: States, decisions: tuple[ParseNode], choices:tuple, natures: tuple,
				 is_final_state: bool, impacts_names, parent = None, probability: np.float64 = None, impacts: np.ndarray = None, cei_top_down: np.ndarray = None, cei_bottom_up: np.ndarray = None):

		super().__init__(id, states, decisions, is_final_state, natures, choices, parent)
		if probability is None or impacts is None or cei_top_down is None or cei_bottom_up is None:
			self.probability, self.impacts = evaluate_expected_impacts(states, len(impacts_names))
			self.cei_top_down:np.ndarray = self.probability * self.impacts
			self.cei_bottom_up:np.ndarray = np.zeros(len(impacts_names), dtype=np.float64)
		else:
			self.probability = probability
			self.impacts = impacts
			self.cei_top_down = cei_top_down
			self.cei_bottom_up = cei_bottom_up

	def dot_str(self, full: bool = True, state: bool = True, executed_time: bool = False, previous_node: States = None):
		result = super().common_dot_str(full, state, executed_time, previous_node)
		if full:
			result += "];\n"

		return result

	def dot_info_str(self):
		label = f"Impacts: {self.impacts}\n"
		if self.probability != 1:
			label += f"Probability: {round(self.probability, 2)}\n"
		label += f"EI Current: {self.cei_top_down}\n"
		if not self.is_final_state:
			label += f"EI Max: {self.cei_bottom_up}\n"

		choice_label = ""
		nature_label = ""

		for choice in self.choices:
			choice_label += f"{choice.name}, "
		for nature in self.natures:
			nature_label += f"{nature.name}, "

		if nature_label != "":
			label += "Nature: " + nature_label[:-2] + "\n"
		if choice_label != "":
			label += "Choice: " + choice_label[:-2] + "\n"

		return self.dot_str(full=False) + "_description", f" [label=\"{label}\", shape=rect];\n"

	def to_dict(self) -> dict:
		base = super().to_dict()
		base.update({
			"probability": self.probability,
			"impacts": self.impacts.tolist(),
			"cei_top_down": self.cei_top_down.tolist(),
			"cei_bottom_up": self.cei_bottom_up.tolist()
		})
		return base