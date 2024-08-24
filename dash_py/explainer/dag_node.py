import math

import pandas as pd


class DagNode:
	# root ---- {('a', 2.5, True), ('b', 3.5, True)} ---->  index = {0,1,2}
	def __init__(self, df: pd.DataFrame):
		self.df = df
		self.index = frozenset(sorted(df.index.to_list()))# Needed for hashing
		# edge: n --{(feature, threshold, lt),('a', 3.5, True)}--> n'
		self.edges = {} # target_node -> edge

		self.tests = set()
		self.splittable = len(set(df['class'])) > 1
		self.best_test = None
		self.best_height = math.inf
		self.visited = False
		self.min_distances_from_root = 0

	def __hash__(self):
		return hash(self.index)

	def __eq__(self, other):
		return self.index == other.index

	def __str__(self):
		return f"{set(self.index)}" # To print '{0, 1, 2}' instead of 'frozenset({0, 1, 2}'

	@staticmethod
	def test_str(test):
		feature, threshold, lt = test
		return f"{feature} {'<' if lt else '>='} {threshold}"

	@staticmethod
	def text_format(text: str, line_length: int):
		parts = []
		current_part = ""
		char_count = 0

		for char in text:
			current_part += char
			char_count += 1
			if char == ',' and char_count >= line_length:
				parts.append(current_part)
				current_part = ""
				char_count = 0

		if current_part:
			parts.append(current_part)

		return "\\n".join(parts)

	@staticmethod
	def edge_str(edge: set):
		result = ""
		for test in sorted(edge):
			result += DagNode.test_str(test) + ", "

		result = result[:-2]
		line_length = int(2 * math.sqrt(len(result)))
		return "{" + DagNode.text_format(result, line_length) + "}"

	def transition_str(self, target_node: 'DagNode', changed=False):
		return f'{("*" if changed else "")}{self} --{self.edge_str(self.edges[target_node])}--> {target_node}'

	def add_node(self, target_node: 'DagNode', test: tuple):
		feature, threshold, lt = test
		self.tests.add((feature, threshold))
		# The edge is a set of tests
		edge = self.edges.get(target_node, None)
		changed = False
		if edge is not None:
			edge.add(test)
			changed = True
		else:
			edge = {test}
		self.edges[target_node] = edge
		return changed

	def get_targets(self, test: tuple):
		feature, threshold = test
		target_t, target_f = None, None
		for target_node, edge in self.edges.items():
			if (feature, threshold) in [(f, t) for f, t, _ in edge]:
				if target_t is None:
					target_t = target_node
				else:
					target_f = target_node
					return target_t, target_f

		raise ValueError("Two children expected but not found")
