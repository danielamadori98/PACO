from datetime import datetime

from paco.explainer.explain_strategy import explain_strategy
from paco.explainer.full_strategy import full_strategy
from paco.explainer.strategy_tree import write_strategy_tree
from paco.explainer.explanation_type import ExplanationType
from paco.parser.tree_lib import CTree, CNode
from paco.execution_tree.execution_tree import ExecutionTree


def build_explained_strategy(parse_tree:CTree, strategy: dict[CNode, dict[CNode, set[ExecutionTree]]], type_strategy: ExplanationType, impacts_names: list, name_svg: str):
    print(f'{datetime.now()} Explain Strategy: ')
    t = datetime.now()
    worst_type_strategy, bdds = explain_strategy(parse_tree, strategy, impacts_names, type_strategy)
    t1 = datetime.now()
    print(f"{t1} Explain Strategy:completed: {(t1 - t).total_seconds()*1000} ms")

    s = f": {worst_type_strategy}"
    if type_strategy == ExplanationType.HYBRID:
        s = f"with worst type of choice{s}\n"
    print(f"{t1} Strategy {s}"+ "".join(f"{choice.name}:\t{bdd.typeStrategy}\n" for choice, bdd in bdds.items()))

    print(f'{t1} StrategyTree: ')
    t = datetime.now()
    strategy_tree, children, expected_impacts, expected_time, _ = full_strategy(parse_tree, bdds, len(impacts_names))
    t1 = datetime.now()
    print(f"{t1} StrategyTree:completed: {(t1 - t).total_seconds()*1000} ms\n")
    print(f"Strategy Expected Impacts: {expected_impacts}\nStrategy Expected Time: {expected_time}")
    write_strategy_tree(strategy_tree)
    #name_svg =  "assets/bpmnSvg/bpmn_"+ str(datetime.timestamp(datetime.now())) +".svg"
    #print_sese_diagram(**bpmn, outfile_svg=name_svg)

    return strategy_tree, expected_impacts, expected_time, [choice.name for choice in bdds.keys()], name_svg
