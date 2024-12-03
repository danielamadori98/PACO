from lark import Lark

"""
    Defining the grammar for SESE diagrams and useful global variables
"""
sese_diagram_grammar = r"""
?start: xor

?xor: parallel
    | xor "/" "[" NAME "]" parallel -> choice
    | xor "^" "[" NAME "]" parallel -> natural

?parallel: sequential
    | parallel "||" sequential  -> parallel

?sequential: region
    | sequential "," region -> sequential    

?region: 
    | NAME   -> task
    | "<" xor ">" -> loop
    | "<" "[" NAME "]"  xor ">" -> loop_probability
    | "(" xor ")"

%import common.CNAME -> NAME
%import common.NUMBER
%import common.WS_INLINE

%ignore WS_INLINE
"""

SESE_PARSER = Lark(sese_diagram_grammar, parser='lalr')
MAX_DELAY = 1
DEFAULT_UNFOLDING_NUMBER = 3

FAILED = False
ADMITTED = True

COMPLETE = 1
CHAR_ACCEPTED = 0
INVALID_CHAR = -1

ALGORITHMS = {  # strategies with labels
    's1': 'PACO',
    's2': 'Strategy 2',
    's3': 'Strategy 3'
}

ALL_SYNTAX = ['^', '/', '||', '<', '>', '[', ']', ',', '', '(', ')'] # all syntax characters available
ALGORITHMS_MISSING_SYNTAX = {
    's1': [],#['<', '>'], # no LOOPs in PACO
    's2': [],
    's3': []
}
#### PATHS ##############################
PATH_IMAGE_BPMN_LARK = 'assets/bpmn.png'
PATH_IMAGE_BPMN_LARK_SVG ='assets/bpmn.svg'

PATH_PARSE_TREE = 'assets/parse_tree.png'
PATH_PARSE_TREE_SVG = 'assets/parse_tree.svg'

PATH_EXECUTION_TREE = 'assets/execution_tree/'
PATH_AUTOMA_STATE = PATH_EXECUTION_TREE + 'state'
PATH_AUTOMA_STATE_DOT = PATH_AUTOMA_STATE + '.dot'
PATH_AUTOMA_STATE_IMAGE = PATH_AUTOMA_STATE + '.png'
PATH_AUTOMA_STATE_IMAGE_SVG = PATH_AUTOMA_STATE + '.svg'

PATH_AUTOMA_STATE_TIME = PATH_EXECUTION_TREE + 'state_time'
PATH_AUTOMA_STATE_TIME_DOT = PATH_AUTOMA_STATE_TIME + '.dot'
PATH_AUTOMA_STATE_TIME_IMAGE = PATH_AUTOMA_STATE_TIME + '.png'
PATH_AUTOMA_STATE_TIME_IMAGE_SVG = PATH_AUTOMA_STATE_TIME + '.svg'

PATH_AUTOMA_STATE_TIME_EXTENDED = PATH_EXECUTION_TREE + 'state_time_extended'
PATH_AUTOMA_STATE_TIME_EXTENDED_DOT = PATH_AUTOMA_STATE_TIME_EXTENDED + '.dot'
PATH_AUTOMA_STATE_TIME_EXTENDED_IMAGE = PATH_AUTOMA_STATE_TIME_EXTENDED + '.png'
PATH_AUTOMA_STATE_TIME_EXTENDED_IMAGE_SVG = PATH_AUTOMA_STATE_TIME_EXTENDED + '.svg'

PATH_AUTOMA_TIME = PATH_EXECUTION_TREE + 'time'
PATH_AUTOMA_TIME_DOT = PATH_AUTOMA_TIME + '.dot'
PATH_AUTOMA_TIME_IMAGE = PATH_AUTOMA_TIME + '.png'
PATH_AUTOMA_TIME_IMAGE_SVG = PATH_AUTOMA_TIME + '.svg'


PATH_EXPLAINER = 'assets/explainer/'
PATH_EXPLAINER_DECISION_TREE = PATH_EXPLAINER + 'decision_tree'
PATH_EXPLAINER_BDD = PATH_EXPLAINER + 'bdd'

PATH_STRATEGY_TREE = 'assets/strategy_tree/'
PATH_STRATEGY_TREE_STATE = PATH_STRATEGY_TREE + 'state'
PATH_STRATEGY_TREE_STATE_DOT = PATH_STRATEGY_TREE_STATE + '.dot'
PATH_STRATEGY_TREE_STATE_IMAGE = PATH_STRATEGY_TREE_STATE + '.png'
PATH_STRATEGY_TREE_STATE_IMAGE_SVG = PATH_STRATEGY_TREE_STATE + '.svg'

PATH_STRATEGY_TREE_STATE_TIME = PATH_STRATEGY_TREE + 'state_time'
PATH_STRATEGY_TREE_STATE_TIME_DOT = PATH_STRATEGY_TREE_STATE_TIME + '.dot'
PATH_STRATEGY_TREE_STATE_TIME_IMAGE = PATH_STRATEGY_TREE_STATE_TIME + '.png'
PATH_STRATEGY_TREE_STATE_TIME_IMAGE_SVG = PATH_STRATEGY_TREE_STATE_TIME + '.svg'

PATH_STRATEGY_TREE_STATE_TIME_EXTENDED = PATH_STRATEGY_TREE + 'state_time_extended'
PATH_STRATEGY_TREE_STATE_TIME_EXTENDED_DOT = PATH_STRATEGY_TREE_STATE_TIME_EXTENDED + '.dot'
PATH_STRATEGY_TREE_STATE_TIME_EXTENDED_IMAGE = PATH_STRATEGY_TREE_STATE_TIME_EXTENDED + '.png'
PATH_STRATEGY_TREE_STATE_TIME_EXTENDED_IMAGE_SVG = PATH_STRATEGY_TREE_STATE_TIME_EXTENDED + '.svg'

PATH_STRATEGY_TREE_TIME = PATH_STRATEGY_TREE + 'time'
PATH_STRATEGY_TREE_TIME_DOT = PATH_STRATEGY_TREE_TIME + '.dot'
PATH_STRATEGY_TREE_TIME_IMAGE = PATH_STRATEGY_TREE_TIME + '.png'
PATH_STRATEGY_TREE_TIME_IMAGE_SVG = PATH_STRATEGY_TREE_TIME + '.svg'


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
LOOP = 'loop_round'
### Automaton parameters
AUTOMATON_TYPE = 'mealy'
### SYNTAX
LOOPS = 'loops'
LOOPS_PROB = 'loops_prob'
ADVERSARIES = 'adversaries' # not yet implemented, neither in the grammar
# BPMN RESOLUTION #######################
RESOLUTION = 300
#############################
# STRATEGY 
STRATEGY = 'strategy'
BOUND = 'bound'


###############
# MODEL
###############
MODEL = "lmstudio-community/Llama-3.1-Nemotron-70B-Instruct-HF-GGUF/Llama-3.1-Nemotron-70B-Instruct-HF-Q4_K_M.gguf"
MODEL_1 = "lmstudio-community/Llama-3.1-Nemotron-70B-Instruct-HF-GGUF"
MODEL_2 = "lmstudio-community/Llama-3.1-Nemotron-70B-Instruct-HF-GGUF/Llama-3.1-Nemotron-70B-Instruct-HF-Q4_K_M.gguf:2"