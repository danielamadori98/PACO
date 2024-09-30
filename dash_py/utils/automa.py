from datetime import datetime

import numpy as np

from utils.env import ALGORITHMS, DURATIONS, IMPACTS #, DELAYS, NAMES, PROBABILITIES
from solver.test_aalpy import automata_search_strategy
from utils import check_syntax as cs
" Here the automata is called to calculate the strategies for the process "
def calc_strat(bpmn:dict, bound:dict, algo:str) -> dict:
    print('calc_strat...')
    # check if the bound is empty
    strategies = {}
    if bpmn['expression'] == '' or bpmn['expression'] == None:
        strategies['error'] = "The expression is empty or None"
        return strategies
    if bound == {} or bound == None:
        strategies['error'] = "The bound  is empty or None"
        return strategies
    bound_list = []
    try:
        bound_list = list(cs.extract_values_bound(bound))
    except Exception as e:
        print(f'Error while parsing the bound: {e}')
        strategies['error'] = f'Error while parsing the bound: {e}'
        return strategies
    if bound_list == []:
        strategies['error'] = "The bound is empty or None"
        return strategies
    # calculate strategies
    if algo == list(ALGORITHMS.keys())[0]:
        strategies, list_choices, name_svg = calc_strategy_paco(bpmn, bound_list)
    elif algo == list(ALGORITHMS.keys())[1]:
        strategies = calc_strategy_algo1(bpmn, bound_list)
    elif algo == list(ALGORITHMS.keys())[2]:
        strategies = calc_strategy_algo2(bpmn, bound_list)
        
    return strategies, list_choices, name_svg



def calc_strategy_paco(bpmn:dict, bound:list[int]) -> dict:
    strategies = {}
    try:
        print(f'{datetime.now()} testing PACO...')
        # replace the duration list with the max duration
        bpmn[DURATIONS] = cs.set_max_duration(bpmn[DURATIONS])         
        print(f'{datetime.now()} bpmn + cpi {bpmn}')
        bound = np.array(bound, dtype=np.float64) # TODO daniel emanuele
        strat, list_choices, name_svg = automata_search_strategy(bpmn, bound)
        if strat:
            if strat.startswith("A strategy") :
                strategies['strat1'] = strat
            elif strat.startswith("Error"):
                strategies['error'] = strat
            if list_choices:
                return strategies, list_choices, name_svg
    except Exception as e:
        print(f'test failed for Paco: {e}')
        strategies['error'] = f'Error while calculating the strategy: {e}'
        return strategies, [], ''
    return strategies, [], name_svg

def calc_strategy_algo1(bpmn:dict, bound:list[int]) -> dict:
    strategies = {}
    return strategies

def calc_strategy_algo2(bpmn:dict, bound:list[int]) -> dict:
    strategies = {}
    return strategies