import pydot
from PIL import Image
import numpy as np
from utils.env import PATH_PARSE_TREE


class CTree:
	def __init__(self, root: 'CNode') -> None:
		self.root = root

	def copy(self) -> 'CTree':
		r = self.root
		if r.type == 'task':
			return CTree(r.copy())
		else:
			r_copy = r.copy()
			left_children = r.children[0].copy()
			left_children.root.parent = r_copy
			right_children = r.children[1].copy()
			right_children.root.parent = r_copy
			r_copy.set_children([left_children, right_children])
			return CTree(r_copy)

class CNode:
	# types = ['task', 'sequential', 'parallel', 'natural', 'choice', 'loop', 'loop_probability']
	isLeaf = True
	children = None

	def __init__(self, parent, index_in_parent, type, id = None, impact = [], non_cumulative_impact = [], probability = None, name = None, short_name = None, ttr = 0, max_delay = 0, duration = 0, incoming_impact_vectors = []) -> None:
		self.id = id
		self.name = name
		self.short_name = short_name
		self.parent = parent
		self.index_in_parent = index_in_parent
		self.type = type
		self.impact = impact
		self.non_cumulative_impact = non_cumulative_impact
		self.probability = probability
		self.ttr = ttr
		self.max_delay = max_delay
		self.duration = duration
		self.incoming_impact_vectors = incoming_impact_vectors

	def copy(self) -> 'CNode':
		return CNode(self.parent, self.index_in_parent, self.type, self.id, self.impact, self.non_cumulative_impact, self.probability, self.name, self.short_name, self.ttr, self.max_delay, self.duration, self.incoming_impact_vectors)

	def set_children(self, children: list[CTree]) -> None:
		self.children = children
		self.isLeaf = False

	def __eq__(self, other: 'CNode') -> bool:
		if isinstance(other, CNode):
			return self.id == other.id
		return False

	def __lt__(self, other: 'CNode') -> bool:
		if isinstance(other, CNode):
			return self.id < other.id
		return False

	def __hash__(self):
		return hash(self.id)

	def __str__(self) -> str:
		return str(self.id)


def print_parse_tree(tree, h = 0, probabilities={}, impacts={}, loop_thresholds = {}, outfile=PATH_PARSE_TREE):
	tree = dot_tree(tree, h, probabilities, impacts, loop_thresholds)
	dot_string = "digraph my_graph{"+ tree +"}"
	graph = pydot.graph_from_dot_data(dot_string)[0]
	graph.write_png(outfile)
	return Image.open(outfile).convert('RGB')

def dot_task(id, name, duration, h=0, imp=None):
	label = name + '\n'
	if imp is not None:
		if h == 0:
			label += str(imp)
		else:
			label += str(imp[0:-h])
			label += str(imp[-h:])
	label += f'\ndur:{duration} id:{id}'

	return f'node_{id}[label="{label}", shape=rectangle style="rounded,filled" fillcolor="lightblue"];'


def dot_choice_gateway(id, label="X"):
	return f'\n node_{id}[shape=diamond label="{label}" style="filled" fillcolor=orange];'

def dot_nature_gateway(id, label="X"):
	return f'\n node_{id}[shape=diamond label="{label}" style="filled" fillcolor=yellowgreen];'

def dot_loop_gateway(id, label="X"):
	return f'\n node_{id}[shape=diamond label="{label}" style="filled" fillcolor=yellow];'

def dot_parallel_gateway(id, label="+"):
	return f'\n node_{id}[shape=diamond label="{label}"];'

def dot_rectangle_node(id, label):
	return f'\n node_{id}[shape=rectangle label="{label}"];'

def dot_tree(t: CTree, h=0, prob={}, imp={}, loops={}, token_is_task=True):
	r = t.root
	if r.type == 'task':
		label = (r.name)
		impact = r.impact
		duration = r.duration
		impact.extend(r.non_cumulative_impact)
		code = dot_task(r.id, label, duration, h, impact if len(impact) != 0 else None) if token_is_task else dot_rectangle_node(r.id, label)
		return code

	label = (r.type)
	code = ""
	child_ids = []
	for i, c in enumerate(r.children):
		dot_code = dot_tree(c, h, prob, imp, loops)
		code += f'\n {dot_code}'
		child_ids.append(c.root.id)
	if label == 'choice':
		if r.max_delay == np.inf: dly_str = 'inf'
		else: dly_str = str(r.max_delay)
		code += dot_choice_gateway(r.id, r.name + ' id:' + str(r.id) + ' dly:' + dly_str)
	elif label == 'natural':
		code += dot_nature_gateway(r.id, r.name + ' id:' + str(r.id))
	elif label == 'loops_prob':
		code += dot_loop_gateway(r.id, label + ' id:' + str(r.id))
	elif label == 'parallel':
		code += dot_parallel_gateway(r.id, label + ' id:' + str(r.id))
	else:
		code += f'\n node_{r.id}[label="{label + " id:" + str(r.id)}"];'
	edge_labels = ['','']
	if label == "natural":
		proba = r.probability
		edge_labels = [f'{proba}', f'{round((1 - proba), 2)}']
	if label == "loops_prob":
		proba = r.probability
		edge_labels = [f'{proba}', f'{round((1 - proba), 2)}']
	for ei,i in enumerate(child_ids):
		edge_label = edge_labels[ei]
		code += f'\n node_{r.id} -> node_{i} [label="{edge_label}"];'
	return code
