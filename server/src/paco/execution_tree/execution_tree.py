from graphviz import Source
from paco.parser.tree_lib import CNode
from paco.saturate_execution.states import States


class ExecutionTree:
	def __init__(self, root: 'ExecutionViewPoint|StrategyViewPoint'):
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


	def create_dot_graph(self, root: 'ExecutionViewPoint|StrategyViewPoint', state: bool, executed_time: bool, diff: bool,
						 previous_node: States = None):
		if not diff:# print all nodes
			previous_node = None

		nodes_id = root.dot_str(state=state, executed_time=executed_time, previous_node=previous_node)
		transitions_id = ""

		impact_id, impact_label = root.dot_info_str()
		transitions_id += f"{root.dot_str(full=False)} -> {impact_id} [label=\"\" color=red];\n"  #style=invis
		nodes_id += impact_id + impact_label

		for transition in root.transitions.keys():
			next_node = root.transitions[transition].root
			x = ""
			for t in transition:
				next = get_sequential_first_task(t[1])
				x += str(t[0].name) + '->' + str(next.id if not next.name else next.name) + ';'
			#x += str(t[0].id) + '->' + str(t[1].id) + ';'
			#x += str(t)[1:-1].replace(',', '->') + ";"

			transitions_id += f"{root.dot_str(full=False)} -> {next_node.dot_str(full=False)} [label=\"{x[:-1]}\"];\n"

			ids = self.create_dot_graph(next_node, state=state, executed_time=executed_time, diff=diff,
										previous_node=root.states)
			nodes_id += ids[0]
			transitions_id += ids[1]

		return nodes_id, transitions_id


	def init_dot_graph(self, state: bool, executed_time: bool, diff: bool):
		result = "digraph automa {\n"

		node, transition = self.create_dot_graph(self.root, state=state, executed_time=executed_time,
												 diff=diff)

		result += node
		result += transition
		result += "__start0 [label=\"\", shape=none];\n"

		starting_node_names = ""
		for n in self.root.decisions:
			n = get_sequential_first_task(n)
			node_name = n.name if n.name else n.id
			starting_node_names += f"{node_name};"

		if len(self.root.choices) + len(self.root.natures) > 0:  #Just if we don't have decisions
			starting_node_names = starting_node_names[:-1] + "->"
			for c in self.root.choices:
				starting_node_names += f"{c.name if c.name else c.id};"
			for n in self.root.natures:
				starting_node_names += f"{n.name if n.name else n.id};"

		result += f"__start0 -> {self.root.dot_str(full=False)}  [label=\"{starting_node_names[:-1]}\"];\n" + "}"
		return result


def get_sequential_first_task(node: CNode):
	if node.type == "sequential":
		return get_sequential_first_task(node.children[0].root)

	return node
