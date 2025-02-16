import numpy as np
from pydot import *
from PIL import Image
from utils.env import PATH_IMAGE_BPMN_LARK, PATH_IMAGE_BPMN_LARK_SVG, RESOLUTION
from paco.parser.tree_lib import CTree

"""
    funzioni prese dal notebook
"""
def print_sese_diagram_explainer(tree, h = 0, probabilities={}, impacts={}, loop_thresholds = {}, outfile=PATH_IMAGE_BPMN_LARK, outfile_svg = PATH_IMAGE_BPMN_LARK_SVG,
                        graph_options = {}, durations = {}, names = {}, delays = {}, impacts_names = [], resolution_bpmn = RESOLUTION, loop_round = {}, loops_prob={}, explainer= False, choices_list =[]):  
    diagram = wrap_sese_diagram(tree=tree, h=h, probabilities= probabilities, impacts= impacts, loop_thresholds=loop_thresholds, durations=durations, names=names, delays=delays, impacts_names=impacts_names, explainer = explainer, choices_list=choices_list)
    global_options = f'graph[ { ", ".join([k+"="+str(graph_options[k]) for k in graph_options])  } ];'
    dot_string = "digraph my_graph{ \n rankdir=LR; \n" + global_options + "\n" + diagram +"}"
    graphs = pydot.graph_from_dot_data(dot_string)    
    graph = graphs[0]  
    print(graph)
    graph.write_svg(outfile_svg)
    graph.write_svg(PATH_IMAGE_BPMN_LARK_SVG)
    #print(graph)  
    graph.set('dpi', resolution_bpmn)
    graph.write_png(outfile)    
    return  Image.open(outfile)   

def dot_sese_diagram(t:CTree, id = 0, h = 0, prob={}, imp={}, loops = {}, dur = {}, imp_names = [], names = {}, choices_list = {}, explainer = False):
    exit_label = ''
    r = t.root
    if r.type == 'Task':
        label = r.name     
        if explainer and label in [choices_list[k][1] for k in list(choices_list.keys())]:
            #adj value id
            choices_list[str(t.children[1])][-1] = id
        return dot_task(id, label, h, imp[label] if label in imp else None, dur[label] if label in dur else None, imp_names), id, id, exit_label
    else:
        label = (r.type)
        code = ""
        child_ids = []
        for i, c in enumerate(r.children):
            if (label != 'natural' or i != 1) and (label != 'choice' or i != 1) and (label != 'loop_probability' or i !=0 ):
                dot_code, enid, exid, tmp_exit_label = dot_sese_diagram(c, last_id, h, prob, imp, loops, dur, imp_names)
                code += f'\n {dot_code}'
                child_ids.append(c.root.id)
                last_id = exid + 1
        if label != "sequential":    
            id_exit = last_id
            if label == "choice":
                code += dot_exclusive_gateway(id_enter, label=r.children[1])
                code += dot_exclusive_gateway(id_exit, label=r.children[1])
            elif label == 'natural':
                code += dot_probabilistic_gateway(id_enter)
                code += dot_probabilistic_gateway(id_exit)
            elif label in {'loop', 'loop_probability'}: 
                code += dot_loop_gateway(id_enter)
                if label == 'loop':
                    code += dot_loop_gateway(id_exit)
                else:
                    code += dot_loop_gateway(id_exit)
            else: 
                label_sym = '+'    
                node_label = f'[shape=diamond label="{label_sym}" style="filled" fillcolor=yellowgreen]'
                code += f'\n node_{id_enter}{node_label};'
                id_exit = last_id
                code += f'\n node_{id_exit}{node_label};'
        else: 
            id_enter = child_ids[0][0]
            id_exit = child_ids[-1][1]    
        edge_labels = ['','','']
        if label == "natural":
            prob_key = t.children[1].value
            edge_labels = [f'{prob[prob_key] if prob_key  in prob else 0.5 }',
                           f'{round(1 - prob[prob_key], 2) if prob_key  in prob else 0.5 }']    
        if label == "loop_probability":
            prob_key = t.children[0].value
            proba = loops[prob_key] if prob_key in loops else 0.5
            edge_labels = ['',f'{proba}']
            exit_label = f'{1-proba}'
        if label != "sequential":
            for ei,i in enumerate(child_ids):
                edge_label = edge_labels[ei]
                edge_style = ''                
                if label in {'choice'} and explainer and choices_list != {} and str(t.children[1]) in list(choices_list.keys()) and i[0] == choices_list[str(t.children[1])][-1]+2:
                    print(f' ids = {i[0]} { choices_list[str(t.children[1])][-1]}')   
                    edge_style = ', style="dashed"'
                code += f'\n node_{id_enter} -> node_{i[0]} [label="{edge_label}" {edge_style}];'
                code += f'\n node_{i[1]} -> node_{id_exit};'
            if label in  {'loop', 'loop_probability'}:  
                code += f'\n node_{id_exit} -> node_{id_enter} [label="{edge_labels[1]}"];'
            # if label in {'choice'} and explainer and str(t.children[1]) in list(choices_list.keys()):
            #     code += f'\n node_{choices_list[t.children[1]][0]} -> node_{choices_list[t.children[1]][1]+2} [style="dashed"];'
        else:
            for ei,i in enumerate(child_ids):
                edge_label = edge_labels[ei]
                if ei != 0:
                    #code += f'\n node_{child_ids[ei - 1][1]} -> node_{i[0]} [label="{edge_label}"];'
                    code += f'\n node_{child_ids[ei - 1][1]} -> node_{i[0]} [label="{exit_labels[0]}"];'
                    exit_label = exit_labels[1]             
    return code, id_enter, id_exit, exit_label

def wrap_sese_diagram(tree, h = 0, probabilities={}, impacts={}, loop_thresholds = {}, durations={}, names={}, delays={}, impacts_names=[],  choices_list = {}, explainer = False):
    code, id_enter, id_exit, exit_label = dot_sese_diagram(tree, 0, h, probabilities, impacts, loop_thresholds, durations, imp_names = impacts_names, names=names, choices_list = choices_list, explainer = explainer)   
    code = '\n start[label="" style="filled" shape=circle fillcolor=palegreen1]' +   '\n end[label="" style="filled" shape=doublecircle fillcolor=orangered] \n' + code
    code += f'\n start -> node_{id_enter};'
    code += f'\n node_{id_exit} -> end [label="{exit_label}"];'
    return code

def get_tasks(t):
    trees = [subtree for subtree in t.iter_subtrees()]
    v = {subtree.children[0].value for subtree in filter(lambda x: x.data == 'task', trees)}
    return v

def dot_task(id, name, h=0, imp=None, dur=None, imp_names = []):
    label = name
    #print(f"impacts in dot task : {imp}")
    if imp is not None: # modifica per aggiungere impatti e durate in modo leggibile 
        if h == 0:
            imp =  ", ".join(f"{key}: {value}" for key, value in zip(imp_names, imp))
            label += f", impacts: {imp}"
            label += f", dur: {str(dur)}"  
        else: 
            label += str(imp[0:-h])
            label += str(imp[-h:]) 
            label += f", dur:{str(dur)}"   
    return f'\n node_{id}[label="{label}", shape=rectangle style="rounded,filled" fillcolor="lightblue"];'

def dot_exclusive_gateway(id, label="X"):
    return f'\n node_{id}[shape=diamond label={label} style="filled" fillcolor=orange];'

def dot_probabilistic_gateway(id, label="N"):
    return f'\n node_{id}[shape=diamond label={label} style="filled" fillcolor=orange];' 

def dot_loop_gateway(id, label="X"):
    return f'\n node_{id}[shape=diamond label={label} style="filled" fillcolor=yellow];' 

def dot_parallel_gateway(id, label="+"):
    return f'\n node_{id}[shape=diamond label={label} style="filled" fillcolor=yellowgreen];'

def dot_rectangle_node(id, label):
    return f'\n node_{id}[shape=rectangle label={label}];'  



def print_sese_custom_tree_explainer(tree:CTree,imp_names, h = 0, probabilities={}, impacts={}, loop_thresholds = {}, outfile="assets/outTree.png", graph_options = {},):
    tree_nt = tree
    tree, end_id = dot_tree(tree,imp_names, h, probabilities, impacts, loop_thresholds)
    tree = '\n start[label="" style="filled" shape=circle fillcolor=palegreen1]' +   '\n end[label="" style="filled" shape=doublecircle fillcolor=orangered] \n' + tree
    tree += f'\n start -> node_{tree_nt.root.id};'
    tree += f'\n node_{end_id} -> end [label="end"];'
    global_options = f'graph[ { ", ".join([k+"="+str(graph_options[k]) for k in graph_options])  } ];'    
    dot_string = "digraph my_graph{ \n rankdir=LR; \n" + global_options + "\n" + tree +"}"
    print(dot_string)
    graph = pydot.graph_from_dot_data(dot_string)
    print(graph)
    if graph:
        graph.write_png(outfile)
        graph.write_svg('assets/treeDiagram.svg')

def dot_task(id, name, duration, imp_names, h=0, imp=[]):
    label = name
    if imp is not None: 
        if h < 1:
            imp =  ", ".join(f"{key}: {value}" for key, value in zip(imp_names, imp))
            label += f", impacts: {imp}"
            label += f", dur: {str(duration)}"  
        else: 
            label += str(imp[0:-h])
            label += str(imp[-h:])             
            label += f", dur:{str(duration)}" 
    return f'node_{id} [label="{label}", shape=rectanble style="rounded,filled" fillcolor="lightblue"];'

def dot_tree(t: CTree,imp_names, h=0, prob={}, imp={}, loops={}, token_is_task=True):
    r = t.root
    if r.type == 'task':
        label = (r.name)
        impact = r.impact
        duration = r.duration
        impact.extend(r.non_cumulative_impact)
        code = dot_task(id=r.id, name=label, duration=duration,imp_names=imp_names, h=h, imp=impact) #if token_is_task else dot_rectangle_node(r.id, label)
        return code, r.id
    else:
        label = (r.type)
        code = ""
        child_ids = []
        for i, c in enumerate(r.children):
            dot_code = dot_tree(t=c, h=h, prob=prob, imp=imp,loops= loops, imp_names=imp_names)
            code += f'\n {dot_code}'
            child_ids.append(c.root.id)
        if label == 'choice':
            # if r.max_delay == np.inf: dly_str = 'inf'
            # else: dly_str = str(r.max_delay)
            code += dot_exclusive_gateway(r.id, r.name) #+ ' dly:' + dly_str
            code += dot_exclusive_gateway(r.children[1], r.name)
        elif label == 'natural':
            code += dot_probabilistic_gateway(r.id)
        elif label == 'loop_probability':
            code += dot_loop_gateway(r.id, label )
        elif label == 'parallel':
            code += dot_parallel_gateway(r.id)        
        else:    
            code += f'\n node_{r.id} [label="{label}"];'
        edge_labels = ['','', ''] 
        if label == "natural":
            prob_key = r.probability
            edge_labels = [f'{prob[prob_key] if prob_key  in prob else 0.5 }',
                           f'{round(1 - prob[prob_key], 2) if prob_key  in prob else 0.5 }'] 
        if label == "loop_probability":
            prob_key = r.probability
            proba = loops[prob_key] if prob_key in loops else 0.5
            edge_labels = ['',f'{proba}']
            exit_label = f'{1-proba}'
        for ei,i in enumerate(child_ids):
            edge_label = edge_labels[ei]
            code += f'\n node_{r.id} -> node_{i} [label="{edge_label}"];' 
        return code, np.argmax(child_ids)