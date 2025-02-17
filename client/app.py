from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash
from api.api import authorization_function, get_agent_definition, invoke_llm
import dash_auth
from dash.dependencies import Input, Output, State
chat_history = []
llm, config_llm = None, None
# docker build -t paco_dash .  && docker run -p 8050:8050 paco_dash
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
            suppress_callback_exceptions=True, 
        )
auth = dash_auth.BasicAuth(
    app,
    auth_func = authorization_function
)
# https://github.com/PietroSala/process-impact-benchmarks
app.layout = html.Div([  
        dcc.Store(id='auth-token-store', storage_type='session'),     
        dcc.Store(id = 'bpmn-lark-store', data={}),
        dcc.Store(id = 'chat-ai-store'),
        html.H1('BPMN+CPI APP!', style={'textAlign': 'center'}),
        dbc.Row(
            [
                dbc.Col(
                    children = [dbc.DropdownMenu([
                            dbc.DropdownMenuItem(
                                f"{page['name']}", href=page["relative_path"]
                            ) for page in dash.page_registry.values()
                            ],
                            label="Menu",
                        ),
                        dash.page_container,
                    ],
                    width=8
                ),
                dbc.Col(
                    children= [
                        html.Div(
                            [
                                # dbc.Button(
                                #     "Open Chat",
                                #     id="collapse-button",
                                #     className="mb-3",
                                #     color="primary",
                                #     n_clicks=0,
                                # ),
                                # dbc.Collapse(
                                    html.Div([
                                        html.H3("Chat with AI"),
                                        dbc.Textarea(id='input-box', placeholder='Type your message here...'),
                                        html.Br(),
                                        dbc.Button(class_name="bi bi-send", id='send-button'),
                                        dcc.Loading(
                                            id="loading-spinner",
                                            type="default",
                                            overlay_style={"visibility":"visible", "filter": "blur(2px)"},
                                            custom_spinner=html.H2(["I'm thinking...", dcc.Loading(id="loading-1", type="default",)]), #,  dbc.Spinner(color="primary")
                                            children=html.Div(id='chat-output-home')
                                        )
                                    ]),
                                #     id="collapse",
                                #     is_open=False,
                                # ),
                            ]
                        )
                    ],
                    width=4
                ),
            ]
        )
        
    ], style={'padding':'30px'})

#######################

## CHAT WITH AI

#######################

@app.callback(
    [Output('chat-output-home', 'children'),],
    [Input('send-button', 'n_clicks')],
    [State('input-box', 'value'), State('auth-token-store', 'data'),
     State('chat-ai-store', 'data')],
    prevent_initial_call=True
)
def update_output(n_clicks, prompt, token, chat_history,  verbose = False):
    if not token:
        return html.P("Please log in first")
    if prompt:
        if verbose:
            print(prompt)
        try:      
            global llm
            if llm is None:
                llm, _ = get_agent_definition(token=token)      
            # Generate the response
            response, chat_history = invoke_llm(llm, prompt, token=token)
            if verbose:
                print(f' response {response}')
           
            # Generate the chat history for display
            chat_display = []
            for user_msg, assistant_msg in chat_history:
                chat_display.append(html.P(f"User: {user_msg}"))
                chat_display.append(dcc.Markdown(f"Assistant: {assistant_msg.replace('[', '[[').replace(']', ']]')}"))
            
            return html.Div(chat_display)
        except Exception as e:
            return html.P(f"Error: {e}")

@app.callback(
    Output('auth-token-store', 'data'),
    Output('chat-ai-store', 'data'),
    Input('auth-token-store', 'modified_timestamp'),
    State('auth-token-store', 'data'),
    prevent_initial_call=False
)
def initialize_token_and_llm(ts, current_token):
    """Initialize token and LLM after successful authentication"""
    if current_token is None:
        # Get token from auth context
        ctx = dash.callback_context
        if hasattr(ctx, 'auth_token'):
            token = ctx.auth_token
            # Initialize LLM with token
            global llm, config_llm
            llm, config_llm = get_agent_definition(token=token)
            return token, {'initialized': True}
    return current_token or {}, {}


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8050", dev_tools_hot_reload=False) # http://157.27.86.122:8050/