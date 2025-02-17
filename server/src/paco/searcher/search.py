from datetime import datetime
import numpy as np

from paco.searcher.create_execution_tree import write_execution_tree
from paco.execution_tree.execution_tree import ExecutionTree
from paco.searcher.found_strategy import found_strategy
from paco.searcher.build_strategy import build_strategy


def search(execution_tree: ExecutionTree, bound: np.ndarray, impacts_names: list, search_only: bool):
    """
    Searches for a feasible strategy in the execution tree that satisfies the given impact bounds.

    Args:
        execution_tree (ExecutionTree): The execution tree representing the BPMN process
        bound (np.ndarray): Array of impact bounds that the strategy must satisfy
        impacts_names (list): List of impact names (e.g., ['cost', 'CO2', 'workHours'])
        search_only (bool): If True, only search for a solution without building the strategy

    Returns:
        tuple: A tuple containing:
            - expected_impacts: The expected impacts of the found strategy (None if no solution)
            - possible_min_solution: The minimum possible solution found
            - solutions: All solutions found during the search
            - strategy: The built strategy (None if search_only=True or no solution found)

    Performance:
        The function prints timing information for the strategy finding and building phases
        in milliseconds.

    Example:
        >>> tree = ExecutionTree(...)
        >>> bound = np.array([100, 50, 200])
        >>> impacts = ['cost', 'CO2', 'workHours']
        >>> exp_impacts, min_sol, sols, strategy = search(tree, bound, impacts, False)
    """
    print(f"{datetime.now()} FoundStrategy:")
    t = datetime.now()
    frontier_solution, expected_impacts, solutions, possible_min_solution = found_strategy([execution_tree], bound)
    t1 = datetime.now()
    print(f"{t1} FoundStrategy:completed: {(t1 - t).total_seconds()*1000} ms")

    if frontier_solution is None:
        #TODO plot_pareto_frontier
        return None, possible_min_solution, solutions, []
    if search_only:
        return expected_impacts, possible_min_solution, solutions, None

    print(f"Success:\t\t{impacts_names}\nBound Impacts:\t{bound}\nExp. Impacts:\t{expected_impacts}")
    # write_execution_tree(execution_tree, frontier_solution)

    print(f'{datetime.now()} BuildStrategy:')
    t = datetime.now()
    _, strategy = build_strategy(frontier_solution)
    t1 = datetime.now()
    print(f"{t1} Build Strategy:completed: {(t1 - t).total_seconds()*1000} ms")
    return expected_impacts, possible_min_solution, solutions, None if len(strategy) == 0 else strategy
