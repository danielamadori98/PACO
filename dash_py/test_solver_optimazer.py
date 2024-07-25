from datetime import datetime
import os
from utils.print_sese_diagram import print_sese_diagram
from utils.automa import calc_strategy_paco


bpmn_ex = {
    "bpmn_linear": [{"expression": "SimpleTask1, Task1",
          "h": 0, 
          "impacts": {"SimpleTask1": [11, 15], "Task1": [4, 2]}, 
          "durations": {"SimpleTask1": [0, 100], "Task1": [0, 100]}, 
          "impacts_names": ["cost", "hours"], 
          "probabilities": {}, "names": {}, "delays": {}, 'loops_prob': {}, 'loops_round': {}
        }, [15, 17]],

    "bpmn_only_choices": [{"expression": "SimpleTask1, (Task1 / [C1] T2)",
          "h": 0, 
          "impacts": {"SimpleTask1": [11, 15], "Task1": [4, 2] , "T2": [3, 3]},
          "durations": {"SimpleTask1": [0, 100], "Task1": [0, 100], "T2":[0, 100]}, 
          "impacts_names": ["cost", "hours"], 
          "probabilities": {}, "names": {'C1':'C1'}, "delays": {"C1": 0},'loops_prob' : {}, 'loops_round': {}
        }, [14, 18]], #[15, 17]
    
    "bpmn_only_natures": [{"expression": "SimpleTask1, (Task1 ^ [N1] T2)",
          "h": 0, 
          "impacts": {"SimpleTask1": [11, 15], "Task1": [4, 2], "T2": [3, 1]}, 
          "durations": {"SimpleTask1": [0, 100], "Task1": [0, 100], "T2":[0, 100]}, 
          "impacts_names": ["cost", "hours"], 
          "probabilities": {"N1": 0.6}, "names": {'N1':'N1'}, "delays": {},'loops_prob' : {}, 'loops_round': {}
        }, [14.7, 16.7]],
    
    "bpmn_seq_choices": [{"expression": "SimpleTask1,  (Task1 / [C1] T2),  (T3 / [C2] T4)",
          "h": 0, 
          "impacts": {"SimpleTask1": [11, 15], "Task1": [4, 2], "T2": [3, 1] , "T3": [8, 9], "T4": [10, 5]}, 
          "durations": {"SimpleTask1": [0, 100], "Task1": [0, 100], "T2":[0, 100], "T3":[0, 100], "T4":[0, 100]},
          "impacts_names": ["cost", "hours"], 
          "probabilities": {}, "names": {'C1':'C1', 'C2':'C2'}, "delays": {"C1": 0, "C2": 0},'loops_prob' : {}, 'loops_round': {}
        }, [23, 26]], #[25, 22], [22, 25], [24, 21]

    "bpmn_seq_natures": [{"expression": "SimpleTask1,  (Task1 ^ [N1] T2),  (T3 ^ [N2] T4)",
          "h": 0, 
          "impacts": {"SimpleTask1": [11, 15], "Task1": [4, 2], "T2": [3, 1] , "T3": [8, 9], "T4": [10, 5]}, 
          "durations": {"SimpleTask1": [0, 100], "Task1": [0, 100], "T2":[0, 100], "T3":[0, 100], "T4":[0, 100]},
          "impacts_names": ["cost", "hours"], 
          "probabilities": {"N1": 0.6, "N2": 0.7}, "names": {}, "delays": {}, 'loops_prob' : {}, 'loops_round': {}
        }, [23.3, 24.4]],

    "bpmn_choices_natures": [{"expression": "(Cutting, ((HP ^ [N1]LP ) || ( FD / [C1] RD)), (HPHS / [C2] LPLS))",
          "h": 0, 
          "impacts": {"Cutting": [11, 15], "HP": [4, 2], "LP": [3, 1] , "FD": [8, 9], "RD": [10, 5] , "HPHS": [4, 7], "LPLS": [3, 8]}, 
          "durations": {"Cutting": 1, "HP": 1, "LP": 1, "FD": 1, "RD":1 , "HPHS": 1, "LPLS": 1}, 
          "impacts_names": ["cost", "hours"], 
          "probabilities": {"N1": 0.6}, "names": {"C1": "C1", "C2": "C2", "N1": "N1"}, "delays": {"C1": 0, "C2": 0},'loops_prob' : {}, 'loops_round': {}
        }, [28.7, 33.7]],

    "bpmn_prof": [{"expression": "(HP ^ [N1]LP ), (HPHS ^ [N2] LPLS), (t1  / [c1] t3)",
        "h": 0,
        "impacts": {"HP": [1, 0, 0, 0], "LP": [0, 1, 0, 0], "HPHS": [0, 0, 1, 0], "LPLS": [0, 0, 0, 1], "t1": [1, 0, 0, 0], "t3": [0, 1, 0, 0]},
        "durations": {"HP": 100, "LP": 100, "HPHS": 100, "LPLS": 100, "t1": 100, "t3": 100},
        "impacts_names": ["cost", "r", "s", "e"],
        "probabilities": {"N1": 0.5, "N2": 0.5},
        "loops_prob": {},
        "names": {"N1": "N1", "N2": "N2", "c1": "c1"},
        "delays": {"c1": 0}, "loop_round": {}
        }, [1, 1, 1, 1]]
}


def test_calc_strategy_paco(bpmn_ex_dicts:dict):

    for key, bpmn in bpmn_ex_dicts.items():
        
        print(f' type bpmn: {key}, strategy {bpmn}')
        
        # per disegnare 
        
        # bpmn_svg_folder = "assets/bpmnTest/"
        # if not os.path.exists(bpmn_svg_folder):
        #     os.makedirs(bpmn_svg_folder)
        # # Create a new SESE Diagram from the input
        # name_svg =  bpmn_svg_folder + "bpmn_"+ str(datetime.timestamp(datetime.now())) +".png"
        # print_sese_diagram(**bpmn, outfile=name_svg) 
        

        # CHIAMA LA FUNZIONE per calcolo paco
        strategies = calc_strategy_paco(bpmn[0], bpmn[1])
        print(f' type bpmn: {key}, strategy {strategies}')

        #ask a string in input if the string is not yes exit
        if input("Do you want to continue? ") != "yes":
            break


test_calc_strategy_paco(bpmn_ex)