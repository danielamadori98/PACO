import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

from src.env import DURATIONS, IMPACTS_NAMES, IMPACTS


def tasks_table(data, tasks):
	if DURATIONS not in data:
		return dash.no_update

	rows = []

	for task in sorted(data[DURATIONS].keys()):
		if task not in tasks:
			continue

		(min_d, max_d) = data[DURATIONS][task]

		impact_inputs = []
		if data[IMPACTS_NAMES]:
			impact_inputs = [
				html.Td(dcc.Input(
					value=data[IMPACTS].get(task, {}).get(impact_name, 0.0),
					type='number', min=0, debounce=True, style={'width': '80px', "border": "none", "padding": "0.4rem"},
					id={'type': f'impact-{impact_name}', 'index': task}
				)) for impact_name in sorted(data[IMPACTS_NAMES])
			]

		row = html.Tr([
						  html.Td(html.Span(task, style={"whiteSpace": "nowrap", "overflow": "hidden", "textOverflow": "ellipsis", "minWidth": "100px", "display": "inline-block"})),
						  html.Td(dcc.Input(value=min_d, type='number', min=0, debounce=True, style={'width': '80px', "border": "none", "padding": "0.4rem"}, id={'type': 'min-duration', 'index': task})),
						  html.Td(dcc.Input(value=max_d, type='number', min=0, debounce=True, style={'width': '80px', "border": "none", "padding": "0.4rem"}, id={'type': 'max-duration', 'index': task})),
					  ] + impact_inputs)
		rows.append(row)

	header_rows = [
		html.Tr([
					html.Th(html.H3("Tasks"), rowSpan=2, style={'vertical-align': 'middle'}),
					html.Th("Duration", colSpan=2, style={'vertical-align': 'middle', 'textAlign': 'center'}),
				] + ([html.Th("Impacts", colSpan=len(data[IMPACTS_NAMES]), style={'vertical-align': 'middle', 'textAlign': 'center'})] if data[IMPACTS_NAMES] else []))
	]

	if data[IMPACTS_NAMES]:
		header_rows.append(html.Tr([
									   html.Th("Min", style={'width': '80px', 'vertical-align': 'middle'}),
									   html.Th("Max", style={'width': '80px', 'vertical-align': 'middle'}),
								   ] + [html.Th(html.Div([
			html.Span(name, style={"whiteSpace": "nowrap", "overflow": "hidden", "textOverflow": "ellipsis", "maxWidth": "80px", "display": "inline-block"}),
			dbc.Button("×", id={'type': 'remove-impact', 'index': name},
					   n_clicks=0, color="danger", size="sm", className="ms-1", style={"padding": "2px 6px"})
		], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'})) for name in sorted(data[IMPACTS_NAMES])])
						   )
	else:
		header_rows.append(html.Tr([
			html.Th("Min", style={'width': '80px', 'vertical-align': 'middle'}),
			html.Th("Max", style={'width': '80px', 'vertical-align': 'middle'})
		]))

	table = [html.Div([
		dbc.Table(
			[html.Thead(header_rows)] + rows,
			bordered=True,
			hover=True,
			responsive=True,
			striped=True,
			style={"width": "auto", "margin": "auto", "borderCollapse": "collapse"},
			className="table-sm"
		)
	], style={
		"display": "inline-block",
		"padding": "10px",
		"border": "1px solid #ccc",
		"borderRadius": "10px",
		"marginTop": "20px"
	}),
		html.Div(id='add-impact-alert', className='mt-2')
	]

	return html.Div(table)
