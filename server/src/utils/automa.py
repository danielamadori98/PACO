import numpy as np
from utils.env import ALGORITHMS
from paco.solver import paco
from utils import check_syntax as cs


def check_input(bpmn:dict, bound:dict):
    bound_list = []
    if bpmn['expression'] == '' or bpmn['expression'] == None:
        return "The expression is empty or None", bound_list
    if bound == {} or bound == None:
        return "The bound is empty or None", bound_list

    try:
        bound_list = list(cs.extract_values_bound(bound))
    except Exception as e:
        return f'Error while parsing the bound: {e}', bound_list

    if bound_list == []:
        return  "The bound is empty or None", bound_list

    return "", bound_list


def calc_strat(bpmn:dict, bound:list, algo:str) -> dict:
    print('calc_strat...')

    # TODO ask emanuele
    if algo == list(ALGORITHMS.keys())[0]:
        bound = np.array(bound, dtype=np.float64)
        text_result, parse_tree, execution_tree, found, min_expected_impacts, max_expected_impacts, choices, name_svg = paco(bpmn, bound)
    elif algo == list(ALGORITHMS.keys())[1]:
        text_result, found, choices, name_svg = calc_strategy_algo1(bpmn, bound)
    elif algo == list(ALGORITHMS.keys())[2]:
        text_result, found, choices, name_svg = calc_strategy_algo2(bpmn, bound)

    return text_result, found, choices, name_svg


def calc_strategy_algo1(bpmn:dict, bound:list):
    return {}, {}, {}, {}

def calc_strategy_algo2(bpmn:dict, bound:list):
    return {}, {}, {}, {}
