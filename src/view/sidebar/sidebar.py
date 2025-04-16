from view.sidebar.bpmn_tab.tab import get_BPMN_CPI_tab
from view.sidebar.strategy_tab.strategy_tab import get_Strategy_tab
from dash import dcc, html

def get_sidebar():
	return html.Div(
		dcc.Tabs(id='bpmn-tabs', value='tab-bpmn', style={'display': 'flex'}, children=[
			get_BPMN_CPI_tab(),
			get_Strategy_tab(),
		]), id="sidebar-container", style={"height": "100%", "overflow": "auto"})