ALGORITHMS = {  # strategies with labels
    'paco': 'PACO',
}

ALGORITHMS_MISSING_SYNTAX = {
    's1': [],
    's2': [],
    's3': []
}
#### PATHS ##############################
PATH_ASSETS = 'assets/'

BPMN_FOLDER = 'bpmnSvg/'
PATH_IMAGE_BPMN_FOLDER = PATH_ASSETS + BPMN_FOLDER

PATH_BPMN = PATH_ASSETS + 'bpmn'
PATH_PARSE_TREE = PATH_ASSETS + 'parse_tree'

PATH_EXECUTION_TREE = PATH_ASSETS + 'execution_tree/'
PATH_EXECUTION_TREE_STATE = PATH_EXECUTION_TREE + 'state'
PATH_EXECUTION_TREE_STATE_TIME = PATH_EXECUTION_TREE + 'state_time'
PATH_EXECUTION_TREE_STATE_TIME_EXTENDED = PATH_EXECUTION_TREE + 'state_time_extended'

PATH_EXECUTION_TREE_TIME = PATH_EXECUTION_TREE + 'time'

PATH_EXPLAINER = PATH_ASSETS + 'explainer/'
PATH_EXPLAINER_DECISION_TREE = PATH_EXPLAINER + 'decision_tree'
PATH_EXPLAINER_BDD = PATH_EXPLAINER + 'bdd'
PATH_STRATEGIES = PATH_ASSETS + 'strategies'

PATH_STRATEGY_TREE = PATH_ASSETS + 'strategy_tree/'
PATH_STRATEGY_TREE_STATE = PATH_STRATEGY_TREE + 'state'
PATH_STRATEGY_TREE_STATE_TIME = PATH_STRATEGY_TREE + 'state_time'
PATH_STRATEGY_TREE_STATE_TIME_EXTENDED = PATH_STRATEGY_TREE + 'state_time_extended'
PATH_STRATEGY_TREE_TIME = PATH_STRATEGY_TREE + 'time'


### args for tree LARK
TASK_SEQ = 'expression'
IMPACTS = 'impacts'
NAMES = 'names'
PROBABILITIES = 'probabilities'
LOOP_THRESHOLD = 'loop_threshold'
DURATIONS = 'durations'
DELAYS = 'delays'
H = 'h'
IMPACTS_NAMES ='impacts_names'
LOOP_ROUND = 'loop_round'
### SYNTAX
LOOP_PROB = 'loop_probability'
# BPMN RESOLUTION #######################
RESOLUTION = 300
#############################
# STRATEGY 
STRATEGY = 'strategy'
BOUND = 'bound'