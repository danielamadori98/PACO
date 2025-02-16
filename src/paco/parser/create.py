from datetime import datetime

from paco.evaluations.evaluate_cumulative_expected_impacts import evaluate_cumulative_expected_impacts
from paco.parser.parse_tree import create_parse_tree
from paco.searcher.create_execution_tree import create_execution_tree, write_execution_tree
from utils.env import IMPACTS_NAMES


def create(bpmn: dict):
    print(f"{datetime.now()} CreateParseTree:")
    t = datetime.now()
    parse_tree = create_parse_tree(bpmn)
    t1 = datetime.now()
    print(f"{t1} CreateParseTree:completed: {(t1 - t).total_seconds()*1000} ms")

    print(f"{datetime.now()} CreateExecutionTree:")
    t = datetime.now()
    execution_tree = create_execution_tree(parse_tree, bpmn[IMPACTS_NAMES])
    t1 = datetime.now()
    print(f"{t1} CreateExecutionTree:completed: {(t1 - t).total_seconds()*1000} ms")
    t = datetime.now()
    evaluate_cumulative_expected_impacts(execution_tree)
    t1 = datetime.now()
    print(f"{t1} CreateExecutionTree:CEI evaluated: {(t1 - t).total_seconds()*1000} ms")
    write_execution_tree(execution_tree)

    return parse_tree, execution_tree
