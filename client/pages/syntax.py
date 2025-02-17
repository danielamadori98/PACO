import asyncio
import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

from api.api import get_bpmn_grammar # , get_image_content
dash.register_page(__name__)

layout = html.Div([
    dcc.Markdown('''
            
        # Syntax and Basic Components
           
        In the following section, you can check the syntax of a BPMN file and the basic components of the language togheter with useful examples. 
        The BPMN language is transformed in a lark grammar and the syntax is checked using the lark parser. 
        Here is the complete grammar:
    '''),

    dcc.Loading(
        id="loading-grammar",
        type="default",
        children=html.Div(id='grammar-content')
    ),
    html.Br(),
    
    html.Div(children=[
       dcc.Markdown('''
            ## Tasks
            The tasks are the most basic element of a BPMN diagram. They represent the work that needs to be done.
            Tasks are defined using the following syntax:
            To define a simple task it is sufficient to digit the name.
            The task can be done by a person or an adversary. To define the task made by the person, just write the name of the task.
            To define the task made by the adversary, just write the name of the task and put a "_" at the beginning.
            Example:
                'Do something' -> simple task made by the person
                '_Do something' -> simple task made by the adversary
                
            '''),
        
        html.Br(),
        html.H3('Task example of a person'),
        html.Img(src=dash.get_asset_url('examples/simple_person_task.png')),
        html.Br(),
        html.H3('Task example of an adversary'),
        html.Img(src=dash.get_asset_url('examples/_SimpleAdversaryTask.png')),
        dbc.Alert("Attention: The adversary here presented is only a theoretical concept. It has not been implemented nor it is found in the aformentioned grammar. ", color="warning"),        
        html.Br(),
        dcc.Markdown('''
               Each task has also a duration and an impact factor. Both are mandatory.
               Duration is an interval that can be between 0 and infinite. If they are not specified, the default values are 0 and infinitive. 
                Otherwise the syntax is the following: 
                (6 Task 9) --> the task will last between 6 and 9 time units.
                (Task 9) ( Task 9) --> the task will last between 0 and 9 time units.
                (6 Task ) --> the task will last between 6 time units and infinitive.
               
                The impact factor is a dictionary of numbers and can be only positive and are cumulative.
               It can be defined as follows:
               Let's say that each task has a cost, number of workers and the hour of labour that are required to conclude the task, 
               so each task will have an impact dictionary as this {"cost": 2, "num_workers":3, "hours": 5}".
               For another task the impact dictionary can be {"cost": 3, "num_workers":2, "hours": 4}.
            '''),
        
        html.Br(),
        html.H3('Example of a task with duration and impact'),
        html.Img(src=dash.get_asset_url('examples/taskimpacts_duration.png')),
        ], style={'padding': 10, 'flex': 1}
    ),
    html.Div(children=[

        dcc.Markdown('''
            ## Gateway
               The gateways are used to control the flow of the process. They are used to merge or split the flow of the process.
               A Gateway represents an intersection where multiple paths converge or diverge.
               The type of gateway can be specified with the following syntax:
               - Exclusive (X): splits the flow in different paths and only one is chosen given a certain condition and is indicated with a X inside the diamond. Here is also marked as orange. In our notation is defined as ^.
               In our notation the consition is defined as Task1 ^ Task2, where ^ is the exclusive gateway.
                - Loops are a particular type of gateways. They are used to repeat a task until a certain condition is met. Here are also marked as yellow.
                In our notation the consition is defined as < SomeTask >, where < ... > is the exclusive gateway.
               - Parallel (+) : all the outgoing flows are followed and in the merging all the activities of the incoming flows must be completed before continuing with the process and it is indicated as + inside the diamond. Here is also marked as green. 
                In our notation the consition is defined as Task1 || Task2, where || is the parallel gateway.
               
        '''),
        
        html.Br(),
        html.H3('Exclusive'),
        html.Img(src=dash.get_asset_url('examples/exclusive.png')),
        html.Br(),
        html.H3('Parallel'),
        html.Img(src=dash.get_asset_url('examples/parallel.png')),
        html.Br(),
        html.H3('Loop'),
        html.Img(src=dash.get_asset_url('examples/loop.png')),
        dbc.Alert("Attention: The loop has not been implemented yet. ", color="warning"),        
        html.Br(),
        dcc.Markdown('''

            ## Choices:
            for each type of gateway, the choices are defined based on who or what takes the decision which are (only for XOR):

            - `^` : Exclusive gateway
                - Person: the decision is taken by a person and no further notetion is needed.
                    - Example: `Task1 ^ Task2`
                - Nature: the decision is taken given a certain probability:
                    - Example: `Task1 ^ [0.3]Task2 ` --> the probability of choosing Task1 is 0.3 and Task2 is 0.7
                - Adversary: the decision is taken by an adversary.
                     - Example: `Task1 ^ []Task2` --> the adversary will choose for this gateway.            
            - < ... > : Loop gateway
                - Person: the decision is taken by a person and no further notetion is needed.
                    - Example: `< Task1 >`
                - Nature: the decision is taken given a certain probability:
                    - Example: `< [0.3]Task1 >` --> the probability of choosing Task1 is 0.3 and Task2 is 0.7
                - Adversary: the decision is taken by an adversary.
                     - Example: `< []Task1 >` --> the adversary will choose for this gateway.
            
            ### Examples natural choice    
                          
        '''),
        html.Img(src=dash.get_asset_url('examples/natural_xor.png')),
    
        ], style={'padding': 10, 'flex': 1}
    ),
    html.Div(children=[
       dcc.Markdown('''
            ## Tasks
            The tasks are the most basic element of a BPMN diagram. They represent the work that needs to be done.
            Tasks are defined using the following syntax:
            To define a simple task it is sufficient to digit the name.
            The task can be done by a person or an adversary. To define the task made by the person, just write the name of the task.
            To define the task made by the adversary, just write the name of the task and put a "_" at the beginning.
            Example:
                'Do something' -> simple task made by the person
                '_Do something' -> simple task made by the adversary
                
            '''),
        
        html.Br(),
        html.H3('Task example of a person'),
        html.Img(src=dash.get_asset_url('examples/simple_person_task.png')),
        html.Br(),
        html.H3('Task example of an adversary'),
        html.Img(src=dash.get_asset_url('examples/_SimpleAdversaryTask.png')),
        html.Br(),
        dcc.Markdown('''
               Each task has also a duration and an impact factor. Both are mandatory.
               Duration is an interval that can be between 0 and infinite. If they are not specified, the default values are 0 and infinitive. 
                Otherwise the syntax is the following: 
                (6 Task 9) --> the task will last between 6 and 9 time units.
                (Task 9) ( Task 9) --> the task will last between 0 and 9 time units.
                (6 Task ) --> the task will last between 6 time units and infinitive.
               
                The impact factor is a dictionary of numbers and can be only positive and are cumulative.
               It can be defined as follows:
               Let's say that each task has a cost, number of workers and the hour of labour that are required to conclude the task, 
               so each task will have an impact dictionary as this {"cost": 2, "num_workers":3, "hours": 5}".
               For another task the impact dictionary can be {"cost": 3, "num_workers":2, "hours": 4}.
            '''),
        
        html.Br(),
        html.H3('Example of a task with duration and impact'),
        html.Img(src=dash.get_asset_url('examples/taskimpacts_duration.png')),
        ], style={'padding': 10, 'flex': 1}
    ),
    # html.Div(id='Problem' ,children=[

    #     dcc.Markdown('''
    #         # Problem
    #         Given a SPIN, and a bound EI decide whether or not there exists a winning strategy S for EI in SPIN.

    #         ## Solution - Automaton
    #         We now show how to build, for any given planning problem 𝑃 , an NFA over Σ that accepts exactly those words that are solutions for 𝑃 . Notice that the 𝑖th element of a
    #         word 𝑤 ∈ Σ∗ can be viewed as a snapshot of the values of the variables at the 𝑖th time-point of the plan associated with 𝑤.
    #         For more info read our paper.
            
    #     '''),
    
    #     ], style={'padding': 10, 'flex': 1}
    # ),
   
])
# layout = html.Div([
#     dcc.Markdown('''
            
#         # Syntax and Basic Components
           
#         In the following section, you can check the syntax of a BPMN file and the basic components of the language togheter with useful examples. 
#         The BPMN language is transformed in a lark grammar and the syntax is checked using the lark parser. 
#         Here is the complete grammar:
#     '''),

#     dcc.Loading(
#         id="loading-grammar",
#         type="default",
#         children=html.Div(id='grammar-content')
#     ),
#     html.Br(),
    
#     html.Div(children=[
#        dcc.Markdown('''
#             ## Tasks
#             The tasks are the most basic element of a BPMN diagram. They represent the work that needs to be done.
#             Tasks are defined using the following syntax:
#             To define a simple task it is sufficient to digit the name.
#             The task can be done by a person or an adversary. To define the task made by the person, just write the name of the task.
#             To define the task made by the adversary, just write the name of the task and put a "_" at the beginning.
#             Example:
#                 'Do something' -> simple task made by the person
#                 '_Do something' -> simple task made by the adversary
                
#             '''),
        
#         html.Br(),
#         html.H3('Task example of a person'),
#         html.Div([
#             html.Img(
#                 id='simple-person-task',
#                 src='',
#                 width="500"
#             ),
#             html.Div(id='simple-person-error')
#         ]),
#         html.Br(),
#         html.H3('Task example of an adversary'),
#         html.Div([
#             html.Img(
#                 id='adversary-task',
#                 src='',
#                 width="500"
#             ),
#             html.Div(id='adversary-error')
#         ]),
#         dbc.Alert("Attention: The adversary here presented is only a theoretical concept. It has not been implemented nor it is found in the aformentioned grammar. ", color="warning"),        
#         html.Br(),
#         dcc.Markdown('''
#                Each task has also a duration and an impact factor. Both are mandatory.
#                Duration is an interval that can be between 0 and infinite. If they are not specified, the default values are 0 and infinitive. 
#                 Otherwise the syntax is the following: 
#                 (6 Task 9) --> the task will last between 6 and 9 time units.
#                 (Task 9) ( Task 9) --> the task will last between 0 and 9 time units.
#                 (6 Task ) --> the task will last between 6 time units and infinitive.
               
#                 The impact factor is a dictionary of numbers and can be only positive and are cumulative.
#                It can be defined as follows:
#                Let's say that each task has a cost, number of workers and the hour of labour that are required to conclude the task, 
#                so each task will have an impact dictionary as this {"cost": 2, "num_workers":3, "hours": 5}".
#                For another task the impact dictionary can be {"cost": 3, "num_workers":2, "hours": 4}.
#             '''),
        
#         html.Br(),
#         html.H3('Example of a task with duration and impact'),
#         html.Div([
#             html.Img(
#                 id='taskimpacts-duration',
#                 src='',
#                 width="500"
#             ),
#             html.Div(id='taskimpacts-error')
#         ]),
#         ], style={'padding': 10, 'flex': 1}
#     ),
#     html.Div(children=[

#         dcc.Markdown('''
#             ## Gateway
#                The gateways are used to control the flow of the process. They are used to merge or split the flow of the process.
#                A Gateway represents an intersection where multiple paths converge or diverge.
#                The type of gateway can be specified with the following syntax:
#                - Exclusive (X): splits the flow in different paths and only one is chosen given a certain condition and is indicated with a X inside the diamond. Here is also marked as orange. In our notation is defined as ^.
#                In our notation the consition is defined as Task1 ^ Task2, where ^ is the exclusive gateway.
#                 - Loops are a particular type of gateways. They are used to repeat a task until a certain condition is met. Here are also marked as yellow.
#                 In our notation the consition is defined as < SomeTask >, where < ... > is the exclusive gateway.
#                - Parallel (+) : all the outgoing flows are followed and in the merging all the activities of the incoming flows must be completed before continuing with the process and it is indicated as + inside the diamond. Here is also marked as green. 
#                 In our notation the consition is defined as Task1 || Task2, where || is the parallel gateway.
               
#         '''),
        
#         html.Br(),
#         html.H3('Exclusive'),
#         html.Div([
#             html.Img(
#                 id='exclusive-gateway',
#                 src='',
#                 width="500"
#             ),
#             html.Div(id='exclusive-error')
#         ]),
#         html.Br(),
#         html.H3('Parallel'),
#         html.Div([
#             html.Img(
#                 id='parallel-gateway',
#                 src='',
#                 width="500"
#             ),
#             html.Div(id='parallel-error')
#         ]),
#         html.Br(),
#         html.H3('Loop'),
#         html.Div([
#             html.Img(
#                 id='loop-gateway',
#                 src='',
#                 width="500"
#             ),
#             html.Div(id='loop-error')
#         ]),
#         dbc.Alert("Attention: The loop has not been implemented yet. ", color="warning"),        
#         html.Br(),
#         dcc.Markdown('''

#             ## Choices:
#             for each type of gateway, the choices are defined based on who or what takes the decision which are (only for XOR):

#             - `^` : Exclusive gateway
#                 - Person: the decision is taken by a person and no further notetion is needed.
#                     - Example: `Task1 ^ Task2`
#                 - Nature: the decision is taken given a certain probability:
#                     - Example: `Task1 ^ [0.3]Task2 ` --> the probability of choosing Task1 is 0.3 and Task2 is 0.7
#                 - Adversary: the decision is taken by an adversary.
#                      - Example: `Task1 ^ []Task2` --> the adversary will choose for this gateway.            
#             - < ... > : Loop gateway
#                 - Person: the decision is taken by a person and no further notetion is needed.
#                     - Example: `< Task1 >`
#                 - Nature: the decision is taken given a certain probability:
#                     - Example: `< [0.3]Task1 >` --> the probability of choosing Task1 is 0.3 and Task2 is 0.7
#                 - Adversary: the decision is taken by an adversary.
#                      - Example: `< []Task1 >` --> the adversary will choose for this gateway.
            
#             ### Examples natural choice    
                          
#         '''),
#         html.Div([
#             html.Img(
#                 id='natural-xor',
#                 src='',
#                 width="500"
#             ),
#             html.Div(id='natural-xor-error')
#         ]),
    
#         ], style={'padding': 10, 'flex': 1}
#     ),
#     html.Div(children=[
#        dcc.Markdown('''
#             ## Tasks
#             The tasks are the most basic element of a BPMN diagram. They represent the work that needs to be done.
#             Tasks are defined using the following syntax:
#             To define a simple task it is sufficient to digit the name.
#             The task can be done by a person or an adversary. To define the task made by the person, just write the name of the task.
#             To define the task made by the adversary, just write the name of the task and put a "_" at the beginning.
#             Example:
#                 'Do something' -> simple task made by the person
#                 '_Do something' -> simple task made by the adversary
                
#             '''),
        
#         html.Br(),
#         html.H3('Task example of a person'),
#         html.Div([
#             html.Img(
#                 id='single-person-task',
#                 src='',
#                 width="500"
#             ),
#             html.Div(id='single-person-task')
#         ]), 
#         html.Br(),
#         # html.H3('Task example of an adversary'),
#         # html.Img(src=dash.get_asset_url('examples/_SimpleAdversaryTask.png')),
#         # html.Br(),
#         # dcc.Markdown('''
#         #        Each task has also a duration and an impact factor. Both are mandatory.
#         #        Duration is an interval that can be between 0 and infinite. If they are not specified, the default values are 0 and infinitive. 
#         #         Otherwise the syntax is the following: 
#         #         (6 Task 9) --> the task will last between 6 and 9 time units.
#         #         (Task 9) ( Task 9) --> the task will last between 0 and 9 time units.
#         #         (6 Task ) --> the task will last between 6 time units and infinitive.
               
#         #         The impact factor is a dictionary of numbers and can be only positive and are cumulative.
#         #        It can be defined as follows:
#         #        Let's say that each task has a cost, number of workers and the hour of labour that are required to conclude the task, 
#         #        so each task will have an impact dictionary as this {"cost": 2, "num_workers":3, "hours": 5}".
#         #        For another task the impact dictionary can be {"cost": 3, "num_workers":2, "hours": 4}.
#         #     '''),
        
#         # html.Br(),
#         # html.H3('Example of a task with duration and impact'),
#         # html.Img(src=dash.get_asset_url('examples/taskimpacts_duration.png')),
#         ], style={'padding': 10, 'flex': 1}
#     ),
#     # html.Div(id='Problem' ,children=[

#     #     dcc.Markdown('''
#     #         # Problem
#     #         Given a SPIN, and a bound EI decide whether or not there exists a winning strategy S for EI in SPIN.

#     #         ## Solution - Automaton
#     #         We now show how to build, for any given planning problem 𝑃 , an NFA over Σ that accepts exactly those words that are solutions for 𝑃 . Notice that the 𝑖th element of a
#     #         word 𝑤 ∈ Σ∗ can be viewed as a snapshot of the values of the variables at the 𝑖th time-point of the plan associated with 𝑤.
#     #         For more info read our paper.
            
#     #     '''),
    
#     #     ], style={'padding': 10, 'flex': 1}
#     # ),
   
# ])

@callback(
    Output('grammar-content', 'children'),
    Input('auth-token-store', 'data'),
    prevent_initial_call=False
)
def update_grammar(token):
    """Update grammar content when token changes"""
    try:
        # Create event loop and run coroutine
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        grammar = loop.run_until_complete(get_bpmn_grammar(token))
        loop.close()
        
        if grammar:
            return dcc.Markdown(f'''
                ```lark
                {grammar}
                ```
            ''')
        return html.Div("Failed to load grammar", style={'color': 'red'})
    except Exception as e:
        return html.Div(f"Error loading grammar: {str(e)}", style={'color': 'red'})
# @callback(
#     [Output('simple-person-task', 'src'),
#      Output('simple-person-error', 'children')],
#     [Input('auth-token-store', 'data')],
#     prevent_initial_call=False
# )
# def update_simple_person_task(token):
#     """Update simple person task image"""
#     try:
#         img_content = get_image_content("simple_person_task", token=token)
#         if img_content:
#             return f'data:image/png;base64,{img_content}', ''
#         return '', html.Div('Failed to load image', style={'color': 'red'})
#     except Exception as e:
#         return '', html.Div(f'Error: {str(e)}', style={'color': 'red'})

# @callback(
#     [Output('adversary-task', 'src'),
#      Output('adversary-error', 'children')],
#     [Input('auth-token-store', 'data')],
#     prevent_initial_call=False
# )
# def update_adversary_task(token):
#     """Update adversary task image"""
#     try:
#         img_content = get_image_content("_SimpleAdversaryTask", token=token)
#         if img_content:
#             return f'data:image/png;base64,{img_content}', ''
#         return '', html.Div('Failed to load image', style={'color': 'red'})
#     except Exception as e:
#         return '', html.Div(f'Error: {str(e)}', style={'color': 'red'})
    

# @callback(
#     [Output('taskimpacts-duration', 'src'),
#      Output('taskimpacts-error', 'children')],
#     [Input('auth-token-store', 'data')],
#     prevent_initial_call=False
# )
# def update_taskimpacts_duration(token):
#     """Update task impacts duration image"""
#     try:
#         img_content = get_image_content("taskimpacts_duration", token=token)
#         if img_content:
#             return f'data:image/png;base64,{img_content}', ''
#         return '', html.Div('Failed to load image', style={'color': 'red'})
#     except Exception as e:
#         return '', html.Div(f'Error: {str(e)}', style={'color': 'red'})
    
# @callback(
#     [Output('exclusive-gateway', 'src'),
#      Output('exclusive-error', 'children')],
#     [Input('auth-token-store', 'data')],
#     prevent_initial_call=False
# )
# def update_exclusive_gateway(token):
#     """Update exclusive gateway image"""
#     try:
#         img_content = get_image_content("exclusive_gateway", token=token)
#         if img_content:
#             return f'data:image/png;base64,{img_content}', ''
#         return '', html.Div('Failed to load image', style={'color': 'red'})
#     except Exception as e:
#         return '', html.Div(f'Error: {str(e)}', style={'color': 'red'})
    
# @callback(
#     [Output('parallel-gateway', 'src'),
#      Output('parallel-error', 'children')],
#     [Input('auth-token-store', 'data')],
#     prevent_initial_call=False
# )
# def update_parallel_gateway(token):
#     """Update parallel gateway image"""
#     try:
#         img_content = get_image_content("parallel_gateway", token=token)
#         if img_content:
#             return f'data:image/png;base64,{img_content}', ''
#         return '', html.Div('Failed to load image', style={'color': 'red'})
#     except Exception as e:
#         return '', html.Div(f'Error: {str(e)}', style={'color': 'red'})
    
# @callback(
#     [Output('loop-gateway', 'src'),
#      Output('loop-error', 'children')],
#     [Input('auth-token-store', 'data')],
#     prevent_initial_call=False
# )
# def update_loop_gateway(token):
#     """Update loop gateway image"""
#     try:
#         img_content = get_image_content("loop_gateway", token=token)
#         if img_content:
#             return f'data:image/png;base64,{img_content}', ''
#         return '', html.Div('Failed to load image', style={'color': 'red'})
#     except Exception as e:
#         return '', html.Div(f'Error: {str(e)}', style={'color': 'red'})
    
# @callback(
#     [Output('natural-xor', 'src'),
#      Output('natural-xor-error', 'children')],
#     [Input('auth-token-store', 'data')],
#     prevent_initial_call=False
# )
# def update_natural_xor(token):
#     """Update natural xor image"""
#     try:
#         img_content = get_image_content("natural_xor", token=token)
#         if img_content:
#             return f'data:image/png;base64,{img_content}', ''
#         return '', html.Div('Failed to load image', style={'color': 'red'})
#     except Exception as e:
#         return '', html.Div(f'Error: {str(e)}', style={'color': 'red'})
    
# @callback(
#     [Output('single-person-task', 'src'),
#      Output('single-person-error', 'children')],
#     [Input('auth-token-store', 'data')],
#     prevent_initial_call=False
# )
# def update_single_person_task(token):
#     """Update single person task image"""
#     try:
#         img_content = get_image_content("single_person_task", token=token)
#         if img_content:
#             return f'data:image/png;base64,{img_content}', ''
#         return '', html.Div('Failed to load image', style={'color': 'red'})
#     except Exception as e:
#         return '', html.Div(f'Error: {str(e)}', style={'color': 'red'})
    