import math
from paco.parser.tree_lib import CTree, CNode
from paco.saturate_execution.states import States, ActivityState


def next_state(tree: CTree, states: States, k: int) -> (States, int):
	root: CNode = tree.root
	#print(f"next_state: " + node_info(root, states))

	if root.type == 'task':
		#print("next_state:Task: " + node_info(root, states))

		remaining_time = root.duration - states.executed_time[root]
		if remaining_time >= k:
			#print(f"next_state:Task:remaining_time >= k: {remaining_time} >= {k}")
			return (States(root,
						ActivityState.ACTIVE if remaining_time > k else ActivityState.COMPLETED_WIHTOUT_PASSING_OVER,
						states.executed_time[root] + k),
					0)

		states.activityState[root] = ActivityState.COMPLETED
		#print(f"next_state:Task:remaining_time < k: {remaining_time} < {k}: ActivityCompleted!")
		return (States(root, ActivityState.COMPLETED, root.duration),
				states.executed_time[root] + k - root.duration)

	leftSubTree = root.children[0]
	rightSubTree = root.children[1]

	if root.type == 'choice' or root.type == 'natural':
		childSx = states.activityState[leftSubTree.root] >= ActivityState.ACTIVE
		if childSx or states.activityState[rightSubTree.root] >= ActivityState.ACTIVE:
			selectedTree = leftSubTree if childSx else rightSubTree
			selectedStates, selectedK = next_state(selectedTree, states, k)

			selectedStates.activityState[root] = selectedStates.activityState[selectedTree.root]
			selectedStates.executed_time[root] = states.executed_time[root] + k - selectedK
			return selectedStates, selectedK

		if root.type == 'natural':
			if k > 0:
				raise Exception("next_state:ExceedingStepsException:Natural")
			#print(f"next_state:Natural:k: 0")
			return States(root, ActivityState.ACTIVE, 0), 0
		else:
			if states.executed_time[root] + k > root.max_delay:
				raise Exception("next_state:ExceedingStepsException:Choice")

			#print(f"next_state:Choice:remaining_time == k: k={k}")
			return States(root, ActivityState.ACTIVE, states.executed_time[root] + k), 0

	if root.type == 'sequential':
		#print("next_state:Sequential: " + node_info(root, states))
		leftStates = States()
		#leftStates = States(leftSubTree.root, ActivityState.COMPLETED, states.executed_time[leftSubTree.root]) #Not needed
		leftK = k
		if states.activityState[leftSubTree.root] != ActivityState.COMPLETED:
			leftStates, leftK = next_state(leftSubTree, states, k)

			#print(f"next_state:Sequential: {node_info(root, states)} leftK: {leftK}")
			#print("next_state:Sequential:LeftStates:")
			#print_states(leftStates)

			if leftStates.activityState[leftSubTree.root] == ActivityState.ACTIVE:
				leftStates.activityState[root] = ActivityState.ACTIVE
				leftStates.executed_time[root] = leftStates.executed_time[leftSubTree.root]
				return leftStates, leftK

		rightStates, rightK = next_state(rightSubTree, states, leftK)
		#print(f"next_state:Sequential: {node_info(root, states)} rightK: {rightK}")
		#print("Sequential:right " + node_info(rightSubTree.root, states))
		#print(f"Sequential:right:{rightCl} {rightK}")

		leftStates.update(rightStates)
		leftStates.activityState[root] = rightStates.activityState[rightSubTree.root]
		leftStates.executed_time[root] = states.executed_time[root] + k - rightK

		return leftStates, rightK

	if root.type == 'parallel':
		#print("next_state:Parallel: " + node_info(root, states))
		leftK = rightK = math.inf
		#leftStates = States()
		#rightStates = States()
		leftStates = States(leftSubTree.root, ActivityState.COMPLETED, states.executed_time[leftSubTree.root])
		rightStates = States(rightSubTree.root, ActivityState.COMPLETED, states.executed_time[rightSubTree.root])

		#print("next_state:Parallel:LeftCheck ")# + node_info(leftSubTree.root, states))
		if states.activityState[leftSubTree.root] != ActivityState.COMPLETED:
			#print("next_state:Parallel:Left")
			leftStates, leftK = next_state(leftSubTree, states, k)
		#print("next_state:Parallel:LeftStates:")
		#print_states(leftStates)

		#print("next_state:Parallel:RightCheck ")# + node_info(rightSubTree.root, states))
		if states.activityState[rightSubTree.root] != ActivityState.COMPLETED:
			#print("next_state:Parallel:Right")
			rightStates, rightK = next_state(rightSubTree, states, k)
		#print("next_state:Parallel:RightStates:")
		#print_states(rightStates)

		if (leftStates.activityState[leftSubTree.root] == ActivityState.ACTIVE or
				rightStates.activityState[rightSubTree.root] == ActivityState.ACTIVE):

			status = ActivityState.ACTIVE
		elif (leftStates.activityState[leftSubTree.root] == ActivityState.COMPLETED and
			  rightStates.activityState[rightSubTree.root] == ActivityState.COMPLETED):

			status = ActivityState.COMPLETED
		else:
			status = ActivityState.COMPLETED_WIHTOUT_PASSING_OVER

		leftStates.update(rightStates)
		leftStates.activityState[root] = status
		leftStates.executed_time[root] = states.executed_time[root] + k - min(leftK, rightK)

		return leftStates, min(leftK, rightK)

	raise Exception(f"next_state:invalid type: ", root)
