import os, sys
import numpy as np

from paco.parser.tree_lib import CNode, CTree, print_parse_tree
from utils import env
from utils.env import LOOPS_PROB, SESE_PARSER, TASK_SEQ, \
	IMPACTS, NAMES, PROBABILITIES, DURATIONS, DELAYS, H

current_directory = os.path.dirname(os.path.realpath('tree_lib.py'))
# Add the current directory to the Python path
sys.path.append(current_directory)

os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'

# sese_diagram_grammar = r"""
# ?start: xor

# ?xor: parallel
#     | xor "/" "[" NAME "]" parallel -> choice
#     | xor "^" "[" NAME "]" parallel -> natural

# ?parallel: sequential
#     | parallel "||" sequential  -> parallel

# ?sequential: region
#     | sequential "," region -> sequential

# ?region:
#      | NAME   -> task
#      | "(@" xor "@)" -> loop
#      | "(@" "[" NAME "]"  xor "@)" -> loop_probability
#      | "(" xor ")"

# %import common.CNAME -> NAME
# %import common.NUMBER
# %import common.WS_INLINE

# %ignore WS_INLINE
# """

#SESE_PARSER = Lark(sese_diagram_grammar, parser='lalr')

# ex = "((Task8 ^ [N1] Task3), (Task1 / [C3] Task2),(Task6 / [C1] Task7))|| (Task9, (Task4 / [C2] Task5))"
# exi = {"Task1": [0,1], "Task2": [0,2], "Task3": [3,3], "Task4": [1,2], "Task5": [2,1], "Task6": [1,0], "Task7": [1,5], "Task8": [0,3], "Task9": [0,3]}
# exd = {"Task1": 1, "Task2": 1,"Task4": 1, "Task3": 1, "Task5": 1, "Task6": 1, "Task7": 1, "Task8": 3, "Task9": 2}
# exn = {"C1": 'Choice1', "C2": 'Choice2', "C3": 'Choice3'}
# exdl = {"C1": np.Inf, "C2": 0, "C3": 0} #maximum delays for the choices
# exp = {"N1": 0.2}

# ex = "(Task1, Task2), (Task3, Task4)"
# exi = {"Task1": [0,1], "Task2": [0,1], "Task3": [0,1], "Task4": [0,1]}
# exd = {"Task1": 1, "Task2": 1, "Task3": 1, "Task4": 1}
# exn = {}
# exdl = {} #maximum delays for the choices
# exp = {}

ex = "(Task1 ^ [N1] Task2) || (Task3 / [C1] Task4)"
exi = {"Task1": [1,1], "Task2": [0,1], "Task3": [2,1], "Task4": [0,1]}
exd = {"Task1": 3, "Task2": 1, "Task3": 3, "Task4": 4}
exn = {"C1": 'Choice1'}
exdl = {"C1": 2} #maximum delays for the choices
exp = {"N1":0.3}

# ex = "Task1 || (Task2, (Task3 / [C1] Task4))"
# exi = {"Task1": [0,1], "Task2": [0,2], "Task3": [3,3], "Task4": [1,2]}
# exd = {"Task1": 1, "Task2": 1,"Task4": 1, "Task3": 1}
# exn = {"C1": 'Choice1'}
# exdl = {"C1": 5} #maximum delays for the choices
# exp = {}

# ex = "(T1 ^ [N1] T2),((T3 / [C1] T4)||(T5 / [C2] T6))"
# exi = {"T1": [2,3], "T2": [4,1], "T3": [2,3], "T4": [3,1], "T5": [2,1], "T6": [1,2]}
# exd = {"T1": 1, "T2": 1,"T4": 1, "T3": 1, "T5":4, "T6":2}
# exn = {"C1": 'Choice1', "C2": 'Choice2'}
# exdl = {"C1": 5, "C2": 2} #maximum delays for the choices
# exp = {"N1": 0.3}

args = {
	'expression': ex,
	'impacts': exi,
	'names': exn,
	'probabilities': exp,
	'loop_thresholds': {},
	'durations': exd,
	'delays': exdl,
	'h': 0
}

# tree = SESE_PARSER.parse(args['expression'])
# custom_tree, last_id = Lark_to_CTree(tree, args['probabilities'], args['impacts'], args['durations'], args['names'], args['delays'], h=args['h'])
# number_of_nodes = last_id + 1


def from_lark_parsed_to_custom_tree(lark_tree, probabilities, impacts, durations, names, delays, loops_prob, loop_round =3, h = 0, loop_thresholds = None, parent = None, index_in_parent = None, id = 0):
	if lark_tree.data == 'task':
		impact = impacts[lark_tree.children[0].value] if lark_tree.children[0].value in impacts else []
		tmp_node = CNode(parent, index_in_parent, lark_tree.data, id = id, name = lark_tree.children[0].value, impact =impact[0:len(impact) - h], non_cumulative_impact =impact[len(impact) - h:], duration=durations[lark_tree.children[0].value])
		return CTree(tmp_node), id
	if lark_tree.data == 'choice':
		tmp_node = CNode(parent, index_in_parent, lark_tree.data, id = id, name=names[lark_tree.children[1].value], short_name=lark_tree.children[1].value, max_delay=delays[lark_tree.children[1].value] if lark_tree.children[1].value in delays.keys() else np.inf)
		left_children, last_id = from_lark_parsed_to_custom_tree(lark_tree.children[0], probabilities, impacts, durations, names, delays, loops_prob, loop_round, id =id + 1, h=h, loop_thresholds=loop_thresholds, parent=tmp_node, index_in_parent=0)
		right_children, last_id = from_lark_parsed_to_custom_tree(lark_tree.children[2], probabilities, impacts, durations, names, delays, loops_prob, loop_round, id =last_id + 1, h=h, loop_thresholds=loop_thresholds, parent=tmp_node, index_in_parent=1)
		tmp_node.set_children([left_children, right_children])
		return CTree(tmp_node), last_id
	if lark_tree.data in {'sequential', 'parallel'}:
		tmp_node = CNode(parent, index_in_parent, lark_tree.data, id = id)
		left_children, last_id = from_lark_parsed_to_custom_tree(lark_tree.children[0], probabilities, impacts, durations, names, delays, loops_prob, loop_round, id =id + 1, h=h, loop_thresholds=loop_thresholds, parent=tmp_node, index_in_parent=0)
		right_children, last_id = from_lark_parsed_to_custom_tree(lark_tree.children[1], probabilities, impacts, durations, names, delays, loops_prob, loop_round, id =last_id + 1, h=h, loop_thresholds=loop_thresholds, parent=tmp_node, index_in_parent=1)
		tmp_node.set_children([left_children, right_children])
		return CTree(tmp_node), last_id
	if lark_tree.data == 'natural':
		tmp_node = CNode(parent, index_in_parent, lark_tree.data, id = id, name=names[lark_tree.children[1].value], probability=probabilities[lark_tree.children[1].value] if lark_tree.children[1].value in probabilities else 0.5)
		left_children, last_id = from_lark_parsed_to_custom_tree(lark_tree.children[0], probabilities, impacts, durations, names, delays, loops_prob, loop_round, id =id + 1, h=h, loop_thresholds=loop_thresholds, parent=tmp_node, index_in_parent=0)
		right_children, last_id = from_lark_parsed_to_custom_tree(lark_tree.children[2], probabilities, impacts, durations, names, delays, loops_prob, loop_round, id =last_id + 1, h=h, loop_thresholds=loop_thresholds, parent=tmp_node, index_in_parent=1)
		tmp_node.set_children([left_children, right_children])
		return CTree(tmp_node), last_id

	#if lark_tree.data == 'loop_probability':
	loop_prob = loops_prob[lark_tree.children[0].value] if lark_tree.children[0].value in loops_prob else 0.5
	number_of_unfoldings = loop_round[lark_tree.children[0].value] if lark_tree.children[0].value in loop_round else env.DEFAULT_UNFOLDING_NUMBER
	num_of_regions_to_replicate = ((number_of_unfoldings - 1)*2) + 1
	# loops have only one child
	id -= 1
	children_list = []
	for dup in range(num_of_regions_to_replicate):
		children, last_id = from_lark_parsed_to_custom_tree(lark_tree.children[1], probabilities, impacts, durations, names, delays, loops_prob, loop_round, id =id + 1, h=h, loop_thresholds=loop_thresholds, parent=None, index_in_parent=0) #parent and index will be modified
		children_list.append(children.copy())
		id = last_id
	unfolded_tree, last_id = recursiveUnfoldingOfLoop(children_list, last_id, parent, index_in_parent, loop_prob)
	return unfolded_tree, last_id


def create_parse_tree(bpmn: dict):
	tree = SESE_PARSER.parse(bpmn[TASK_SEQ]) # Parse the task sequence from the BPMN diagram
	#print(tree.pretty)

	# Convert the parsed tree into a custom tree and get the last ID
	parse_tree, last_id = from_lark_parsed_to_custom_tree(tree, bpmn[PROBABILITIES], bpmn[IMPACTS], bpmn[DURATIONS], bpmn[NAMES], bpmn[DELAYS], h=bpmn[H], loops_prob=bpmn[LOOPS_PROB])
	print_parse_tree(parse_tree)
	return parse_tree


def recursiveUnfoldingOfLoop(children_list, id, parent, index_in_parent, loop_prob):
	#recursive construction of the final unfolded tree
	if len(children_list) == 1:
		return children_list[0], id

	tmp = CNode(parent, index_in_parent, "natural", id=id+1, probability=loop_prob)
	seq = CNode(tmp, 0, "sequential", id=id+2)
	last_id = id+2
	unfolded, last_id = recursiveUnfoldingOfLoop(children_list[2:], last_id, seq, 1, loop_prob)
	children_list[0].root.parent = seq
	children_list[0].root.index_in_parent = 0
	children_list[1].root.parent = tmp
	children_list[1].root.index_in_parent = 1
	seq.set_children([children_list[0], unfolded])
	tmp.set_children([CTree(seq), children_list[1]])
	return CTree(tmp), last_id
