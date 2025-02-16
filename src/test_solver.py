import numpy as np
from utils.env import TASK_SEQ, H, IMPACTS, DURATIONS, IMPACTS_NAMES, PROBABILITIES, NAMES, DELAYS, LOOPS_PROB, LOOP
from paco.solver import paco



bpmn_ex = {
    "decision_based_example" : [{
        TASK_SEQ: '((T1 /[C1] T2) || (( (T3 ^[N2] T4), TU1) ^[N1] ( (T5 ^[N3] T6), TU2)))',
        IMPACTS_NAMES: ['a', 'b'],
        IMPACTS: {'T1': [3, 1], 'T2': [1, 3], 'T3': [2, 0], 'T4': [0, 2], 'TU1': [3, 1], 'T5': [2, 0], 'T6': [0, 2], 'TU2': [1, 3]},
        DURATIONS: {'T1': [0, 1], 'T2': [0, 1], 'T3': [0, 1], 'T4': [0, 1], 'TU1': [0, 1], 'T5': [0, 1], 'T6': [0, 1], 'TU2': [0, 1]},
        PROBABILITIES: {'N2': 0.2, 'N1': 0.3, 'N3': 0.4},
        LOOPS_PROB: {},
        NAMES: {'C1': 'C1', 'N2': 'N2', 'N1': 'N1', 'N3': 'N3'},
        DELAYS: {'C1': 1}, LOOP: {}, H: 0,
        }, [5, 6]
    ],
    "unavoidable_example" : [{
        TASK_SEQ: '((T1 /[C1] T2) || ((TD1, (T3 ^[N2] T4), TU1) ^[N1] (TD2,  (T5 ^[N3] T6), TU2)))',
        IMPACTS_NAMES: ['a', 'b'],
        IMPACTS: {'T1': [3, 1], 'T2': [1, 3], 'T3': [2, 0], 'T4': [0, 2], 'TU1': [3, 1], 'T5': [2, 0], 'T6': [0, 2], 'TU2': [1, 3], 'TD1': [0, 0], 'TD2': [0, 0]},
        DURATIONS: {'T1': [0, 1], 'T2': [0, 1], 'T3': [0, 1], 'T4': [0, 1], 'TU1': [0, 1], 'T5': [0, 1], 'T6': [0, 1], 'TU2': [0, 1], 'TD1': [0, 2], 'TD2': [0, 2]},
        PROBABILITIES: {'N2': 0.2, 'N1': 0.3, 'N3': 0.4},
        LOOPS_PROB: {},
        NAMES: {'C1': 'C1', 'N2': 'N2', 'N1': 'N1', 'N3': 'N3'},
        DELAYS: {'C1': 1}, LOOP: {}, H: 0,
    }, [5, 6]
    ],
    "natures of natures": [{
        TASK_SEQ: "(Task1 ^ [N1] T2) ^[N] (T3 ^ [N2] T4)",
        H: 0,
        IMPACTS: {"Task1": [4, 2], "T2": [3, 1] , "T3": [8, 9], "T4": [10, 5]},
        DURATIONS: {"Task1": [0, 100], "T2":[0, 100], "T3":[0, 100], "T4":[0, 100]},
        IMPACTS_NAMES: ["cost", "hours"],
        PROBABILITIES: {"N": 0.5, "N1": 0.6, "N2": 0.7}, NAMES: {"N":"N", "N1":"N1", "N2":"N2"}, DELAYS: {}, LOOPS_PROB : {}, LOOP: {}
    }, [23.3, 24.4]],

    "just task, no strategy (no choice)": [{
        TASK_SEQ: "T1, T2",
        H: 0,
        IMPACTS: {"T1": [11, 15], "T2": [4, 2]},
        DURATIONS: {"T1": [0, 100], "T2": [0, 100]},
        IMPACTS_NAMES: ["cost", "hours"],
        PROBABILITIES: {}, NAMES: {}, DELAYS: {}, LOOPS_PROB: {}, LOOP: {}
    }, [15, 17]],

    "one choice, strategy with one obligated decision (current impacts)": [{
        TASK_SEQ: "T0, (T1 / [C1] T2)",
        H: 0,
        IMPACTS: {"T0": [11, 15], "T1": [4, 2] , "T2": [3, 3]},
        DURATIONS: {"T0": [0, 100], "T1": [0, 100], "T2":[0, 100]},
        IMPACTS_NAMES: ["cost", "hours"],
        PROBABILITIES: {}, NAMES: {'C1':'C1'}, DELAYS: {"C1": 0},LOOPS_PROB : {}, LOOP: {}
    }, [14, 18]], #[15, 17]

    "only natures, no strategy (no choice)": [{
        TASK_SEQ: "SimpleTask1, (Task1 ^ [N1] T2)",
        H: 0,
        IMPACTS: {"SimpleTask1": [11, 15], "Task1": [4, 2], "T2": [3, 1]},
        DURATIONS: {"SimpleTask1": [0, 100], "Task1": [0, 100], "T2":[0, 100]},
        IMPACTS_NAMES: ["cost", "hours"],
        PROBABILITIES: {"N1": 0.6}, NAMES: {'N1':'N1'}, DELAYS: {},LOOPS_PROB : {}, LOOP: {}
    }, [14.7, 16.7]],

    "sequential choices": [{TASK_SEQ: "SimpleTask1,  (Task1 / [C1] T2),  (T3 / [C2] T4)",
                            H: 0,
                            IMPACTS: {"SimpleTask1": [11, 15], "Task1": [4, 2], "T2": [3, 1] , "T3": [8, 9], "T4": [10, 5]},
                            DURATIONS: {"SimpleTask1": [0, 100], "Task1": [0, 100], "T2":[0, 100], "T3":[0, 100], "T4":[0, 100]},
                            IMPACTS_NAMES: ["cost", "hours"],
                            PROBABILITIES: {}, NAMES: {'C1':'C1', 'C2':'C2'}, DELAYS: {"C1": 0, "C2": 0},LOOPS_PROB : {}, LOOP: {}
                            }, [23, 26]], #[23, 26], [25, 22], [22, 25], [24, 21]

    "bpmn_seq_natures": [{
        TASK_SEQ: "SimpleTask1,  (Task1 ^ [N1] T2),  (T3 ^ [N2] T4)",
        H: 0,
        IMPACTS: {"SimpleTask1": [11, 15], "Task1": [4, 2], "T2": [3, 1] , "T3": [8, 9], "T4": [10, 5]},
        DURATIONS: {"SimpleTask1": [0, 100], "Task1": [0, 100], "T2":[0, 100], "T3":[0, 100], "T4":[0, 100]},
        IMPACTS_NAMES: ["cost", "hours"],
        PROBABILITIES: {"N1": 0.6, "N2": 0.7}, NAMES: {"N1":"N1", "N2":"N2"}, DELAYS: {}, LOOPS_PROB : {}, LOOP: {}
    }, [23.3, 24.4]],

    "bpmn_choices_natures": [{
        TASK_SEQ: "(Cutting, ((HP ^ [N1]LP ) || ( FD / [C1] RD)), (HPHS / [C2] LPLS))",
        H: 0,
        IMPACTS: {"Cutting": [11, 15], "HP": [4, 2], "LP": [3, 1] , "FD": [8, 9], "RD": [10, 5] , "HPHS": [4, 7], "LPLS": [3, 8]},
        DURATIONS: {"Cutting": 1, "HP": 1, "LP": 1, "FD": 1, "RD":1 , "HPHS": 1, "LPLS": 1},
        IMPACTS_NAMES: ["cost", "hours"],
        PROBABILITIES: {"N1": 0.6},
        NAMES: {"C1": "C1", "C2": "C2", "N1": "N1"},
        DELAYS: {"C1": 0, "C2": 0}, LOOPS_PROB : {}, LOOP: {}
    }, [26, 33.3]],

    "bpmn_prof": [{
        TASK_SEQ: "(HP ^ [N1]LP ), (HPHS ^ [N2] LPLS), (t1  / [c1] t3)",
        H: 0,
        IMPACTS: {"HP": [1, 0, 0, 0], "LP": [0, 1, 0, 0], "HPHS": [0, 0, 1, 0], "LPLS": [0, 0, 0, 1], "t1": [1, 0, 0, 0], "t3": [0, 1, 0, 0]},
        DURATIONS: {"HP": 100, "LP": 100, "HPHS": 100, "LPLS": 100, "t1": 100, "t3": 100},
        IMPACTS_NAMES: ["cost", "r", "s", "e"],
        PROBABILITIES: {"N1": 0.5, "N2": 0.5},
        LOOPS_PROB: {},
        NAMES: {"N1": "N1", "N2": "N2", "c1": "c1"},
        DELAYS: {"c1": 0}, LOOP: {}
    }, [1, 1, 1, 1]],

    "bpmn_unavoidable_tasks": [{
        TASK_SEQ: "(TaskA ^ [C1] TaskB), Task2",
        H: 0,
        IMPACTS: {"TaskA": [10], "TaskB": [10], "Task2": [10]},
        DURATIONS: {"TaskA": 100, "TaskB": 100, "Task2": 100},
        IMPACTS_NAMES: ["cost"],
        PROBABILITIES: {"C1": 0.5}, NAMES: {"C1": "C1"}, DELAYS: {"C1": 0},LOOPS_PROB : {}, LOOP: {}
    }, [20]],

    "bpmn_unavoidable_tasks2": [{
        TASK_SEQ: "(HP ^ [N1]LP ), (HPHS ^ [N2] LPLS), (t1  / [c1] t3), t4",
        H: 0,
        IMPACTS: {"HP": [1, 0, 0, 0], "LP": [0, 1, 0, 0], "HPHS": [0, 0, 1, 0], "LPLS": [0, 0, 0, 1], "t1": [1, 0, 0, 0], "t3": [0, 1, 0, 0], "t4": [1, 1, 1, 1]},
        DURATIONS: {"HP": 100, "LP": 100, "HPHS": 100, "LPLS": 100, "t1": 100, "t3": 100, "t4": 100},
        IMPACTS_NAMES: ["cost", "r", "s", "e"],
        PROBABILITIES: {"N1": 0.5, "N2": 0.5},
        LOOPS_PROB: {},
        NAMES: {"N1": "N1", "N2": "N2", "c1": "c1"},
        DELAYS: {"c1": 0}, LOOP: {}
    }, [2, 2, 2, 2]],

    "bpmn_unavoidable_tasks3": [{
        TASK_SEQ: "(HP ^ [N1]LP ), (HPHS ^ [N2] LPLS), (t1  / [c1] t3), t4, t5",
        H: 0,
        IMPACTS: {"HP": [1, 0, 0, 0], "LP": [0, 1, 0, 0], "HPHS": [0, 0, 1, 0], "LPLS": [0, 0, 0, 1], "t1": [1, 0, 0, 0], "t3": [0, 1, 0, 0], "t4": [1, 1, 1, 1], "t5": [1, 1, 1, 1]},
        DURATIONS: {"HP": 100, "LP": 100, "HPHS": 100, "LPLS": 100, "t1": 100, "t3": 100, "t4": 100, "t5": 100},
        IMPACTS_NAMES: ["cost", "r", "s", "e"],
        PROBABILITIES: {"N1": 0.5, "N2": 0.5},
        LOOPS_PROB: {},
        NAMES: {"N1": "N1", "N2": "N2", "c1": "c1"},
        DELAYS: {"c1": 0}, LOOP: {}
    }, [3, 3, 3, 3]],

    "choice not explained": [{
        TASK_SEQ: "(T1, ((TA_N1 ^[N1] TB_N1) || ( TA_C1 / [C1] TB_C1)), (TA_C2 / [C2] TB_C2))",
        H: 0,
        IMPACTS: {"T1": [11, 15], "TA_N1": [4, 2], "TB_N1": [3, 1] , "TA_C1": [8, 9], "TB_C1": [10, 5] , "TA_C2": [4, 7], "TB_C2": [3, 8]},
        DURATIONS: {"T1": 1, "TA_N1": 1, "TB_N1": 1, "TA_C1": 1, "TB_C1":1 , "TA_C2": 1, "TB_C2": 1},
        IMPACTS_NAMES: ["cost", "hours"],
        PROBABILITIES: {"N1": 0.6}, NAMES: {"C1": "C1", "C2": "C2", "N1": "N1"},
        DELAYS: {"C1": 0, "C2": 0},LOOPS_PROB : {}, LOOP: {}
    }, [30, 30]],

    #TODO
    "complete coloring strategy tree example": [{
        TASK_SEQ: "(T1, ((TA_N1 ^[N1] TB_N1) || ( TA_C1 / [C1] TB_C1)), ((TA_C2 / [C2] TB_C2) || (TA_N2 ^[N2] TB_N2)))",
        H: 0,
        IMPACTS: {"T1": [1, 2], "TA_N1": [10, 5], "TB_N1": [5, 10] , "TA_C1": [20, 10], "TB_C1": [21, 11] , "TA_C2": [20, 10], "TB_C2": [10, 20], "TA_N2": [10, 5], "TB_N2": [5, 10]},
        DURATIONS: {"T1": 1, "TA_N1": 1, "TB_N1": 1, "TA_C1": 1, "TB_C1":1 , "TA_C2": 1, "TB_C2": 1, "TA_N2": 1, "TB_N2": 1},
        IMPACTS_NAMES: ["A", "B"],
        PROBABILITIES: {"N1": 0.6, "N2": 0.5}, NAMES: {"C1": "C1", "C2": "C2", "N1": "N1", "N2": "N2"},
        DELAYS: {"C1": 1, "C2": 0},LOOPS_PROB : {}, LOOP: {}
    }, [57, 48]],

    # TODO "multi condition BDD"
}
def test(name, bpmn, bound):
    print('Type bpmn: ', name)
    text_result, parse_tree, execution_tree, found, min_expected_impacts, max_expected_impacts, choices, name_svg = paco(bpmn, np.array(bound, dtype=np.float64))
    print('Type bpmn: ', name)


def test_calc_strategy_paco(bpmn_ex_dicts:dict, selected:int = -1):
    if selected == -1:
        for name, example in bpmn_ex_dicts.items():
            print(name, example[0], example[1])
            test(name, example[0], example[1])
            #ask a string in input if the string is not yes exit
            answer = input("Do you want to continue? (yes/no): ")
            if answer != "yes" and answer != "y":
                break
    else:
        name, example = list(bpmn_ex_dicts.items())[selected]
        test(name, example[0], example[1])


bpmn_paper_example = {
    "Figure 1": [{
        TASK_SEQ: "(Cutting, ((Bending, (HP^[N1]LP)) || (Milling, (FD/[C1]RD))), (HPHS / [C2] LPLS))",
        H: 0,
        IMPACTS: {"Cutting": [10, 1], "Bending": [20, 1], "Milling": [50, 1], "HP": [5, 4], "LP": [8, 1], "FD": [30, 1], "RD": [10, 1], "HPHS": [40, 1], "LPLS": [20, 3]},
        DURATIONS: {"Cutting": [0, 1], "Bending": [0, 1], "Milling": [0, 1], "HP": [0, 2], "LP": [0, 1], "FD": [0, 1], "RD": [0, 1], "HPHS": [0, 1], "LPLS": [0, 2]},
        IMPACTS_NAMES: ["electric energy", "worker hours"],
        PROBABILITIES: {"N1": 0.2}, NAMES: {"C1": "C1", "C2": "C2", "N1": "N1"}, DELAYS: {"C1": 0, "C2": 0},LOOPS_PROB : {}, LOOP: {}
        }, [135, 9]], #[135, 7]
    #TODO loops
    "loop": [{
        TASK_SEQ: "(T1, ((Bending, (HP^[N1]LP)) || (Milling, (FD/[C1]RD))))",
        H: 0,
        IMPACTS: {"T1": [10, 1], "Bending": [20, 1], "Milling": [50, 1], "HP": [5, 4], "LP": [8, 1], "FD": [30, 1], "RD": [10, 1]},
        DURATIONS: {"T1": [0, 1], "Bending": [0, 1], "Milling": [0, 1], "HP": [0, 2], "LP": [0, 1], "FD": [0, 1], "RD": [0, 1]},
        IMPACTS_NAMES: ["electric energy", "worker hours"],
        PROBABILITIES: {"N1": 0.2}, NAMES: {"C1": "C1", "N1": "N1"}, DELAYS: {"C1": 0},LOOPS_PROB : {}, LOOP: {}
    }, [100, 7]],
    "Explainer Figure": [{
        TASK_SEQ: "((t0p0 ^[p0] t1p0), (t0p5 /[p5] t1p5), (tp11, (t0p13 /[p13] t1p13),(t0p24 /[p24] t1p24) || (t0p12, tp20, (t0p22 ^[p22] t1p22) ^[p12] t1p12, tp21, (t0p23 ^ [p23] t1p23) ) ) )",
        H: 0,
        IMPACTS: {"t0p0": [2, 1, 0, 0, 0, 0], "t1p0": [1, 2, 0, 0, 0, 0], "t0p5": [1, 2, 0, 0, 0, 0], "t1p5": [2, 1, 0, 0, 0, 0], "tp11": [4, 2, 0, 0, 0, 0],
                  "t0p13": [0, 0, 8, 0, 0, 0], "t1p13": [0, 0, 0, 8, 0, 0], "t0p24": [0, 0, 0, 0, 5, 0], "t1p24": [0, 0, 0, 0, 0, 5], "t0p12": [3, 5, 0, 0, 0, 0],
                  "t1p12": [3, 5, 0, 0, 0, 0], "t0p23": [0, 0, 0, 0, 8, 1], "t1p23": [0, 0, 0, 0, 1, 8], "t0p22": [0, 0, 0, 0, 8, 1], "t1p22": [0, 0, 0, 0, 1, 8],
                  "tp20": [0, 0, 8, 0, 0, 0], "tp21": [0, 0, 0, 8, 0, 0]},

        DURATIONS: {"t0p0": [0, 1], "t1p0": [0, 1], "t0p5": [0, 1], "t1p5": [0, 1], "tp11": [0, 1], "t0p13": [0, 1], "t1p13": [0, 1], "t0p24": [0, 1], "t1p24": [0, 1], "t0p12": [0, 2], "t1p12": [0, 2], "t0p23": [0, 1], "t1p23": [0, 1], "t0p22": [0, 1], "t1p22": [0, 1], "tp20": [0, 1], "tp21": [0, 1] },
        IMPACTS_NAMES: ["A", "B", "C", "D", "E", "F"],
        PROBABILITIES: {"p0": 0.5, "p12": 0.5, "p22": 0.99, "p23":0.01}, NAMES: {"p0": "p0", "p5": "p5", "p13": "p13", "p12": "p12", "p24": "p24", "p22": "p22", "p23": "p23"}, DELAYS: {"p5": 0, "p13": 0, "p24": 0},LOOPS_PROB : {}, LOOP: {}
    }, [10,10,8,8,7,7]],
    "Explainer Figure_1": [{
        TASK_SEQ: "((p1 ^[p0] p2), (p6 /[p5] p7), ((p16, (p28 /[p21] p29),(p35 /[p33] p36)) || (p19, p26 ^[p15] p20, p27) || (p13, (p22 ^[p17] p23) ^[p11] p14, (p24 ^ [p18] p25) )) )",
        H: 0,
        IMPACTS: {"p1": [2, 1, 0, 0, 0, 0], "p2": [1, 2, 0, 0, 0, 0], "p6": [1, 2, 0, 0, 0, 0], "p7": [2, 1, 0, 0, 0, 0], "p16": [0, 0, 0, 0, 0, 0],
                  "p35": [0, 0, 8, 0, 0, 0], "p36": [0, 0, 0, 8, 0, 0], "p28": [0, 0, 0, 0, 5, 0], "p29": [0, 0, 0, 0, 0, 5], "p19": [0, 0, 0, 0, 0, 0],
                  "p20": [0, 0, 0, 0, 0, 0], "p24": [0, 0, 0, 0, 8, 1], "p25": [0, 0, 0, 0, 1, 8], "p22": [0, 0, 0, 0, 8, 1], "p23": [0, 0, 0, 0, 1, 8],
                  "p13": [0, 0, 0, 0, 0, 0], "p14": [0, 0, 0, 0, 0, 0], "p26": [0, 0, 8, 0, 0, 0], "p27": [0, 0, 0, 8, 0, 0]},
        DURATIONS: {"p1": [0, 1], "p2": [0, 1], "p6": [0, 1], "p7": [0, 1], "p16": [0, 1], "p28": [0, 1],
                    "p29": [0, 1], "p35": [0, 1], "p36": [0, 1], "p19": [0, 3], "p20": [0, 3], "p24": [0, 1],
                    "p25": [0, 1], "p22": [0, 1], "p23": [0, 1], "p13": [0, 1], "p14": [0, 1], "p26": [0, 1], "p27": [0, 1],
                    },
        IMPACTS_NAMES: ["A", "B", "C", "D", "E", "F"],
        PROBABILITIES: {"p0": 0.5, "p11": 0.5, "p15": 0.5, "p17": 0.99, "p18":0.01},
        NAMES: {"p0": "p0", "p5": "p5", "p11": "p11", "p15": "p15", "p17": "p17", "p18": "p18", "p21": "p21", "p33":"p33"},
        DELAYS: {"p5": 0, "p21": 0, "p33": 0},LOOPS_PROB : {}, LOOP: {}
    }, [3.5, 3.5,11, 12, 9.5, 9.5]], #[3,3,8,8,7,7]
    'example_final': [
        {'impacts_names': ['costo', 'CO2', 'oreLavorate'],
        'expression': 'arrivoCommessa, ( checkInventario, (recuperoMateriale /[TuttoPresente] (ordinareMancante, recuperoMateriale, ( materialeIn3gg ^[arrivoVeloceMateriale] materialein7gg)))  || organizzaImpresaLogistica, (aspetta1gg ^[CamionDisponibile] aspetta10gg )), assemblaSemiLavorato, dipingi, testProdotto, ( (imballaProdotto, caricaCamion) /[vaBene]  eliminaProdotto)', 
        'impacts': {
            'arrivoCommessa': [0, 0, 0], 
            'checkInventario': [4, 6, 6], 
            'recuperoMateriale': [16, 13, 16], 
            'ordinareMancante': [11, 2, 1], 
            'materialeIn3gg': [40, 1, 56], 
            'materialein7gg': [31, 45, 6], 
            'organizzaImpresaLogistica': [1, 3, 8], 
            'aspetta1gg': [0, 0, 0], 
            'aspetta10gg': [0, 0, 0], 
            'assemblaSemiLavorato': [44, 15, 0], 
            'dipingi': [100, 78, 16], 
            'testProdotto': [84, 64, 14], 
            'imballaProdotto': [1, 0, 64], 
            'caricaCamion': [5, 4, 5], 
            'eliminaProdotto': [82, 5, 7]
        }, 
        'durations': {
            'arrivoCommessa': [0, 100], 
            'checkInventario': [0, 100], 
            'recuperoMateriale': [0, 100], 
            'ordinareMancante': [0, 100], 
            'materialeIn3gg': [0, 100], 'materialein7gg': [0, 100], 'organizzaImpresaLogistica': [0, 100], 'aspetta1gg': [0, 100], 'aspetta10gg': [0, 100], 'assemblaSemiLavorato': [0, 100], 'dipingi': [0, 100], 'testProdotto': [0, 100], 'imballaProdotto': [0, 100], 'caricaCamion': [0, 100], 'eliminaProdotto': [0, 100]
        }, 
        'probabilities': {
            'arrivoVeloceMateriale': 0.75, 
            'CamionDisponibile': 0.5
        },
        'loops_prob': {}, 
        'names': {
            'TuttoPresente': 'TuttoPresente', 
            'arrivoVeloceMateriale': 'arrivoVeloceMateriale', 
            'CamionDisponibile': 'CamionDisponibile', 
            'vaBene': 'vaBene'
        }, 
        'delays': {
            'TuttoPresente': 0,
            'vaBene': 0
        }, 'loop_round': {}, 'h': 0}
    , [0, 0, 0,]],
    'example_final_2': [
        {'impacts_names': ['costo', 'CO2', 'oreLavorate'], 'expression': 'PrepareMaterials, ( (AssemblePartA ^[MaterialTypeSelection] ( (InspectPartA, CalibratePartA) /[AssemblyDecision] (ReworkPartA, CalibratePartA) ) ) || ( (StartPartB /[InspectionDecision](InspectPartB, ApprovePartB)) /[RepairDecision] (RepairPartB, ScrapPartB))),  ( (AssemblePartB ^[MachineCondition]  (CalibrateMachine, ReplaceTool) )/[AssemblyCheck] (InspectAssembly,  (TestAssembly ^[TestProtocol] (RunProtocolA, RunProtocolB) ))),  ((((PackageProduct, (LogInspectionResults /[PackagingDecision] RejectPackaging)) || ((FinalizeLabel, (PrintLabel ^[LabelTypeSelection]  DrawLabel)) /[FinalApproval] (ApproveLabel, ((ShipProduct ^[ShippingMode] ((LoadTruck /[LoadingDecision](VerifyLoad, AdjustLoad)), (SealContainer /[SealCheck](CheckSeal, Reseal))))))))))', 'impacts': {'PrepareMaterials': [0, 0, 0], 'AssemblePartA': [0, 0, 0], 'InspectPartA': [0, 0, 0], 'CalibratePartA': [0, 0, 0], 'ReworkPartA': [0, 0, 0], 'StartPartB': [0, 0, 0], 'InspectPartB': [0, 0, 0], 'ApprovePartB': [0, 0, 0], 'RepairPartB': [0, 0, 0], 'ScrapPartB': [0, 0, 0], 'AssemblePartB': [0, 0, 0], 'CalibrateMachine': [0, 0, 0], 'ReplaceTool': [0, 0, 0], 'InspectAssembly': [0, 0, 0], 'TestAssembly': [0, 0, 0], 'RunProtocolA': [0, 0, 0], 'RunProtocolB': [0, 0, 0], 'PackageProduct': [0, 0, 0], 'LogInspectionResults': [0, 0, 0], 'RejectPackaging': [0, 0, 0], 'FinalizeLabel': [0, 0, 0], 'PrintLabel': [0, 0, 0], 'DrawLabel': [0, 0, 0], 'ApproveLabel': [0, 0, 0], 'ShipProduct': [0, 0, 0], 'LoadTruck': [0, 0, 0], 'VerifyLoad': [0, 0, 0], 'AdjustLoad': [0, 0, 0], 'Sea': [0, 0, 0], 'CalibratePartA': [0, 0, 0], 'ReworkPartA': [0, 0, 0], 'StartPartB': [0, 0, 0], 'InspectPartB': [0, 0, 0], 'ApprovePartB': [0, 0, 0], 'RepairPartB': [0, 0, 0], 'ScrapPartB': [0, 0, 0], 'AssemblePartB': [0, 0, 0], 'CalibrateMachine': [0, 0, 0], 'ReplaceTool': [0, 0, 0], 'InspectAssembly': [0, 0, 0], 'TestAssembly': [0, 0, 0], 'RunProtocolA': [0, 0, 0], 'RunProtocolB': [0, 0, 0], 'PackageProduct': [0, 0, 0], 'LogInspectionResults': [0, 0, 0], 'RejectPackaging': [0, 0, 0], 'FinalizeLabel': [0, 0, 0], 'PrintLabel': [0, 0, 0], 'DrawLabel': [0, 0, 0], 'ApproveLabel': [0, 0, 0], 'ShipProduct': [0, 0, 0], 'LoadTruck': [0, 0, 0], 'VerifyLoad': [0, 0, 0], 'AdjustLoad': [0, 0, 0], 'SearateMachine': [0, 0, 0], 'ReplaceTool': [0, 0, 0], 'InspectAssembly': [0, 0, 0], 'TestAssembly': [0, 0, 0], 'RunProtocolA': [0, 0, 0], 'RunProtocolB': [0, 0, 0], 'PackageProduct': [0, 0, 0], 'LogInspectionResults': [0, 0, 0], 'RejectPackaging': [0, 0, 0], 'FinalizeLabel': [0, 0, 0], 'PrintLabel': [0, 0, 0], 'DrawLabel': [0, 0, 0], 'ApproveLabel': [0, 0, 0], 'ShipProduct': [0, 0, 0], 'LoadTruck': [0, 0, 0], 'VerifyLoad': [0, 0, 0], 'AdjustLoad': [0, 0, 0], 'SeatPackaging': [0, 0, 0], 'FinalizeLabel': [0, 0, 0], 'PrintLabel': [0, 0, 0], 'DrawLabel': [0, 0, 0], 'ApproveLabel': [0, 0, 0], 'ShipProduct': [0, 0, 0], 'LoadTruck': [0, 0, 0], 'VerifyLoad': [0, 0, 0], 'AdjustLoad': [0, 0, 0], 'SealContainer': [0, 0, 0], 'CheckSeal': [0, 0, 0], 'Reseal': [0, 0, 0]}, 'durations': {'PrepareMaterials': [0, 100], 'AssemblePartA': [0, 100], 'InspectPartA': [0, 100], 'CalibratePartA': [0, 100], 'ReworkPartA': [0, 100], 'StartPartBlContainer': [0, 0, 0], 'CheckSeal': [0, 0, 0], 'Reseal': [0, 0, 0]}, 'durations': {'PrepareMaterials': [0, 100], 'AssemblePartA': [0, 100], 'InspectPartA': [0, 100], 'CalibratePartA': [0, 100], 'ReworkPartA': [0, 100], 'StartPartB': [0, 100], 'InspectPartB': [0, 100], 'ApprovePartB': [0, 100], 'RepairPartB': [0, 100], 'ScrapPartB': [0, 100], 'AssemblePartB': [0, 100], 'CalibrateMachine': [0, 100], 'ReplaceTool': [0, 100], 'InspectAssembly': [0, 100], 'TestAssembly': [0, 100], 'RunProtocolA': [0, 100], 'RunProtocolB': [0, 100], 'PackageProduct': [0, 100], 'LogInspectionResults': [0, 100], 'RejectPackaging': [0, 100], 'FinalizeLabel': [0, 100], 'PrintLabel': [0, 100], 'DrawLabel': [0, 100], 'ApproveLabel': [0, 100], 'ShipProduct': [0, 100], 'LoadTruck': [0, 100], 'VerifyLoad': [0, 100], 'AdjustLoad': [0, 100], 'SealContainer': [0, 100], 'CheckSeal': [0, 100], 'Reseal': [0, 100]}, 'probabilities': {'MaterialTypeSelection': 0.5, 'MachineCondition': 0.5, 'TestProtocol': 0.5, 'LabelTypeSelection': 0.5, 'ShippingMode': 0.5}, 'loops_prob': {}, 'names': {'MaterialTypeSelection': 'MaterialTypeSelection', 'AssemblyDecision': 'AssemblyDecision', 'Inspection': 0.5, 'MachineCondition': 0.5, 'TestProtocol': 0.5, 'LabelTypeSelection': 0.5, 'ShippingMode': 0.5}, 'loops_prob': {}, 'names': {'MaterialTypeSelection': 'MaterialTypeSelection', 'AssemblyDecision': 'AssemblyDecision', 'InspectionDecision': 'InspectionDecision', 'RepairDecision': 'RepairDecision', 'MachineCondition': 'MachineCondition', 'AssemblyCheck': 'AssemblyCheck', 'TestProtocol': 'TestProtocol', 'PackagingDecision': 'PackagingDecision', 'LabelTypeSelection': 'LabelTypeSelection', 'FinalApproval': 'FinalApproval', 'ShippingMode': 'ShippingMode', 'LoadingDecision': 'LoadingDecision', 'SealCheck': 'SealCheck'}, 'delays': {'AssemblyDecision': 0, 'InspectionDecision': 0, 'RepairDecision': 0, 'AssemblyCheck': 0, 'PackagingDecision': 0, 'FinalApproval': 0, 'LoadingDecision': 0, 'SealCheck': 0}, 'loop_round': {}, 'h': 0}, [0, 0, 0,]],
}


test_calc_strategy_paco(bpmn_paper_example, 3)



#test_calc_strategy_paco(bpmn_ex, 0)

#test_calc_strategy_paco(bpmn_ex, 0) #decision_based example
#test_calc_strategy_paco(bpmn_ex, 1) #unavoidable example
#test_calc_strategy_paco(bpmn_ex, 4) #current impacts (one obligated decision)
#test_calc_strategy_paco(bpmn_ex, 8) #current impacts


#test_calc_strategy_paco(bpmn_ex, 14)


#Testing StrategyTree:
#test_calc_strategy_paco(bpmn_ex, 0) # Not pruned ask if okay, decision_based example
#test_calc_strategy_paco(bpmn_ex, 1) # Not pruned ask if okay, unavoidable example
#test_calc_strategy_paco(bpmn_ex, 4) # Okay, current impacts (one obligated decision)
#test_calc_strategy_paco(bpmn_ex, 6) # Okay, current impacts (two obligated decision)
#test_calc_strategy_paco(bpmn_ex, 8) # Okay, current impacts
#test_calc_strategy_paco(bpmn_ex, 9) # Not pruned ask if okay, all leaves in the frontier
