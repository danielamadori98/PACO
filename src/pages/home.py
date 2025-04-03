import json
import dash
from dash import html, dcc, Input, Output,State, callback
import dash_bootstrap_components as dbc

from utils import check_syntax as cs
from env import ALGORITHMS, BOUND, DELAYS, DURATIONS, H, IMPACTS, PATH_BPMN, PATH_STRATEGY_TREE_STATE_TIME, STRATEGY, EXPRESSION

dash.register_page(__name__, path='/')
# SimpleTask1, Task1 || Task, Task3 ^ Task9
bpmn_lark = {
    EXPRESSION: '',
    H: 0, # indicates the index of splitting to separate non-cumulative and cumulative impacts impact_vector[0:H] for cumulative impacts and impact_vector[H+1:] otherwise
    IMPACTS: {},
    DURATIONS: {},
}
strategy_d = {}
min_duration = 0
max_duration = 100
value_interval = [min_duration, max_duration]
marks = {j: str(j) for j in range(min_duration, int(max_duration), 10) if j != 0}
spinner = dbc.Spinner(color="primary", type="grow", fullscreen=True)

def layout():
    return html.Div([
        html.Div(id='logging'),
        html.Div(id='logging-strategy'),
        # dbc.Alert("Disclaimer: This is not a definitive app! There may be some bugs or placeholders. Please be careful! Moreover, the BPMN dimension supported varies among machines. So for big BPMN choose a powerful PC. ", color="warning"),
        dcc.Tabs(id="tabs", value='tab-1', children=[
            ################################
            ### DEFINING THE BPMN + DCPI ###
            ################################
            dcc.Tab(label='BPMN', value='tab-1', children=[
                html.Div([
                    html.H1('Insert your BPMN here:'),
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select a JSON File')
                        ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },
                        # Allow multiple files to be uploaded
                        multiple=True
                    ),
                    html.Div(id='output-data-upload'),
                    html.Br(),
                    html.P("""Here is an example of a BPMN complete diagram: Task0, (Task1 || Task4), (Task3 ^[N1] Task9, Task8 /[C1] Task2)"""),
                    html.Br(),
                    html.Div(id='loaded-bpmn-file'),
                    html.Br(),
                    dcc.Textarea(value='', id = 'input-bpmn', style={'width': '100%'}, ), # persistence = True persistence è obbligatoria altrimenti quando ricarica la pagina (cioè ogni valta che aggiorna il graph )        
                    html.Br(),                    
                    dbc.Button('Next', id='go-to-define-durations'),
                ])
            ]),
            dcc.Tab(label='Durations', value='tab-2', children=[
                html.Div([
                    html.Div(id='task-duration'),
                    dbc.Button('Back', id='back-to-load-bpmn'),
                    dbc.Button('Next', id='go-to-impacts-bpmn'),
                ])
            ]),
            dcc.Tab(label='CPI: Impacts', value='tab-3', children=[
                html.Div([
                    html.P('Insert the impacts list of the tasks in the following format: cost, hours. IF for some task the impacts are not defined they will be put 0 by default.'),
                    dcc.Textarea(value='cost',  id = 'input-impacts', persistence=True, style={'width': '100%'}),
                    html.Div(id='impacts-table'),
                    dbc.Button('Back', id='back-to-durations'),
                    dbc.Button('Next', id='go-to-cp'),
                ])
            ]),
            dcc.Tab(label='CPI: Choices and natures', value='tab-4', children=[
                html.Div([                   
                    html.P('Insert the probabilities for each natural choice, if any. The values have to be between 0 and 1.'),
                    html.Div(id= 'probabilities'),
                    html.Br(),
                    html.P('Insert the delays for each natural choice, if any. The values have to be between 0 and 100.'),
                    html.Div(id= 'delays'),
                    html.Br(),    
                    html.P('Insert the number of maximum loops round, if any. The value have to be between 1 and 100.'),    
                    html.Div(id= 'loops'),
                    html.Br(),
                    dbc.Button('Back', id='back-to-impacts'),
                    dbc.Button('Next', id='go-to-show-bpmn'),
                ])
            ]),
            ###############################
            ### BPMN DIAGRAM USING LARK ###
            ###############################
            dcc.Tab(label='Show BPMN', value='tab-5', children=[
                dbc.Button('Create diagram', id='create-diagram-button'),
                
                html.Div([
                    html.H3("BPMN diagram in lark:"),
                    #html.Img(id='lark-diagram1', src= 'assets/graph.svg', style={'height': '500', 'width': '1000'}),
                    html.Iframe(id="lark-frame",
                                src='',#PATH_IMAGE_BPMN_LARK_SVG,
                                style={'height': '100%', 'width': '100%'}
                                # style={"height": "70vh", "width": "95vw", 'border':'none'}
                                ), #style={'height': '100%', 'width': '100%'}
                    # html.Embed(
                    #     id="lark-frame",
                    #     src=PATH_IMAGE_BPMN_LARK_SVG,
                    #     type="image/svg+xml",
                    #     style={"height": "100vh", "width": "100vw", "border": "none"}
                    # ),
                    html.Br(),
                    # download diagram as svg
                    html.A('Download diagram as SVG', id='download-diagram', download='diagram.svg', href=PATH_BPMN+'.svg', target='_blank'),
                    html.Br(),
                    dbc.Button('Back', id='back-to-load-cpi'),
                    dbc.Button('Next', id='go-to-define-strategy'),
                ]),
                html.Br(),
            ]),
            ################
            ### STRATEGY ###
            ################
            dcc.Tab(label='Define Strategy',  value='tab-6', children=[
                html.Div([
                    
                    html.Div(id="strategy", children=[
                        html.H3("Choose the algorithm to use:"),
                        dcc.Dropdown(
                            id='choose-strategy',
                            options=[
                                {'label': value, 'value': key}
                                for key, value in ALGORITHMS.items()
                            ],
                            value= list(ALGORITHMS.keys())[0] # default value
                        ),
                        html.H3('Insert the bound'),                        
                        html.Div(id= 'choose-bound-dict'),
                        html.Br(),
                        html.Br(),
                        dbc.Button('Find strategy', id='find-strategy-button'),                        
                    ]),
                    html.Br(),
                    html.Br(),    
                    dbc.Button('Back', id='back-to-show-bpmn'),
                    dbc.Button('Next', id='go-to-show-strategy'), 
                ])
            ]),
            dcc.Tab(label='Show Strategy',  value='tab-7', children=[
                html.Div([
                    html.Div(
                        children = [
                            dcc.Loading(
                                id="loading-strategy",
                                children=[html.Div([html.Div(id="strategy-founded")])],
                                type="circle", #'graph', 'cube', 'circle', 'dot', 'default'
                                # fullscreen=True,
                            )
                        ]
                    ), 
                    dbc.Button('Back', id='back-to-strategy'),
                    dbc.Button('Next', id='go-to-download'),                   
                ])
            ]),
            dcc.Tab(label='Download data',  value='tab-8', children=[
                ########################
                ### DOWNLOAD EXAMPLE ###
                ########################
                html.Div(id="download-example", children=[
                    html.H1("Download the example:"), 
                    dbc.Checklist(
                        options=[
                            {"label": "BPMN + CPI", "value": 1},
                            {"label": "Bound", "value": 2},
                            {"label": "Strategy", "value": 3},
                        ],
                        value=[1, 2],
                        id="switches-input",
                        switch=True,
                    ),
                    dbc.Button("Download", id="btn-download"),
                    dcc.Download(id="download"),
                    html.Br(),
                    dbc.Button('Back', id='back-to-show-strategy'),
                    # dbc.Button('Next', id='go-to-define-strategy'),
                ]),
            ]),
            # dcc.Tab(label='Strategy Explainer', value='tab-6', children=[
            #     html.Div([
            #         html.H1("Explaining strategy"),
            #           dbc.Button('Back', id='back-to-load-bpmn'),
            #     ])
            # ])
        ]),   
        
    ]
)

######################
## NAVIGATE TABS  ###
######################

@callback(
    Output('tabs', 'value', allow_duplicate=True),
    [
     Input('back-to-load-bpmn', 'n_clicks'),
     Input('go-to-show-bpmn', 'n_clicks'),
     Input('back-to-load-cpi', 'n_clicks'),
     Input('go-to-define-strategy', 'n_clicks'),
     Input('back-to-show-bpmn', 'n_clicks'),
     Input('go-to-show-strategy', 'n_clicks'),
     Input('back-to-strategy', 'n_clicks'), 
     Input('go-to-define-durations', 'n_clicks'),
     Input('go-to-impacts-bpmn', 'n_clicks'),
     Input('back-to-durations', 'n_clicks'),
     Input('go-to-cp', 'n_clicks'),
     Input('back-to-impacts', 'n_clicks'),
     Input('back-to-show-strategy', 'n_clicks'),
     Input('go-to-download', 'n_clicks'),
    ],
    prevent_initial_call=True
)
def navigate_tabs(*args):
    ctx = dash.callback_context

    if not ctx.triggered:
        # No button was clicked yet
        return 'tab-1'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Mapping from button ID to tab value
    tab_mapping = {
        'go-to-define-durations': 'tab-2',
        'go-to-impacts-bpmn': 'tab-3',
        'back-to-durations': 'tab-2',
        'go-to-cp': 'tab-4',
        'back-to-impacts': 'tab-3',
        'go-to-define-cpi': 'tab-2',
        'back-to-load-bpmn': 'tab-1',
        'go-to-show-bpmn': 'tab-5',
        'back-to-load-cpi': 'tab-4',
        'go-to-define-strategy': 'tab-6',
        'back-to-show-bpmn': 'tab-5',
        'go-to-show-strategy': 'tab-7',
        'back-to-strategy': 'tab-6',
        'back-to-show-strategy': 'tab-7',
        'go-to-download': 'tab-8',
    }

    return tab_mapping.get(button_id, 'tab-1')  # Default to 'tab-1' if button_id is not found



@callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

######################
# FIND THE STRATEGY

########################
@callback(
    [Output('strategy-founded', 'children'), Output('logging-strategy', 'children'), Output('tabs','value', allow_duplicate=True)],
    Input('find-strategy-button', 'n_clicks'),
    State('choose-strategy', 'value'),
    State('choose-bound-dict', 'children'),
    State('bpmn-lark-store', 'data'),
    prevent_initial_call=True
)
def find_strategy(n_clicks, algo:str, bound:dict, bpmn_lark:dict):
    """This function is when the user search a str."""
    if bound == {} or bound == None:
        return [html.P(f'Insert a bound dictionary to find the strategy.'),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("ERROR"),  class_name="bg-danger"),
                        dbc.ModalBody("Insert a bound dictionary to find the strategy."),
                    ],
                    id="modal",
                    is_open=True,
                ),'tab-6'
            ]
    expected_impacts = None
    choices = None
    text_result = ''
    try:
        text_result, bound = cs.check_input(bpmn_lark, bound)
        print(bound)
        code, resp_json = calc_strat(bpmn_lark, bound, algo, token='neonrejieji')
        print(resp_json)
        print(code)
        if code != 200:
            return [html.P(f'Insert a bound dictionary to find the strategy.'),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("ERROR"),  class_name="bg-danger"),
                        dbc.ModalBody(str(resp_json)),
                    ],
                    id="modal",
                    is_open=True,
                ),'tab-6'
            ]
        strategy_d[BOUND] = resp_json[BOUND]
        expected_impacts = resp_json['expected_impacts']
        choices = resp_json['choices']
        text_result = resp_json['text_result']
    except Exception as e:
        error = True
        text_result = str(e)

    if expected_impacts is None:
        return [None,
            dbc.Modal([
                        dbc.ModalHeader(dbc.ModalTitle("Strategy not found"),  class_name="bg-info"),
                        dbc.ModalBody("No strategy found for the given bound. Try with another bound.\n"+ text_result),
                    ],
                id="modal", is_open=True,
            ),'tab-6']

    # # TODO save the strategy for the download
    # #strategy_d[STRATEGY] = ....

    s = [
        html.P(text_result),
        html.Iframe(src='', style={'height': '100%', 'width': '100%'}),
        html.A('Download strategy diagram as SVG', id='download-diagram', download='strategy.svg', href=PATH_STRATEGY_TREE_STATE_TIME+'.png', target='_blank'),
    ]

    if choices:
        navigate_tabs('go-to-show-strategy')
        list_choices_excluded = list(set(list(bpmn_lark[DELAYS].keys())) - set(choices))
        s.append(dcc.Tabs(
            children=[dcc.Tab(label=c, children=[html.Iframe(src=f'assets/explainer/decision_tree_{c}.svg', style={'height': '100%', 'width': '100%'})]) for c in choices]
        ))
        if list_choices_excluded:
            s.append(dbc.Alert(f" The choices: {list_choices_excluded} are not visited by the explainer. ", color='warning'))

        return [html.Div(s), None, 'tab-7']

    #TODO: create the strategy tree
    s.append(dbc.Alert(" All the choices presents are not visited by the explainer. ", color='warning'))
    return [html.Div(s), None, 'tab-7']


######################

# DOWNLOAD 

######################

@callback(
    Output("download", "data"),
    Input("btn-download", "n_clicks"),
    State('switches-input', 'value'),
    State('bpmn-lark-store', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, switches, bpmn_lark):
    print(f' in dwonlaoad {switches}')
    content = {}
    for el in switches: 
        if el == 1:
            content['bpmn'] = bpmn_lark
        elif el == 2:
            content['bound'] = strategy_d[BOUND]
        elif el == 3:
            content['strategy'] = strategy_d[STRATEGY]
    content = json.dumps(content)
    return dict(content=content, filename="bpmn_cpi_strategy.json")
