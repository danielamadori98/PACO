from dash import html
from view.sidebar.strategy_tab.table.create_advance_table import render_table


def strategy_results(result: str, expected_impacts: list, guaranteed_bounds: list, possible_min_solution: list, bdds: list, sorted_impact_names: list, sort_by=None, sort_order="asc"):
	elements = [
		html.H5("Result", className="mt-2"),
		html.P(result, className="text-body"),
		html.Hr()
	]

	if expected_impacts:
		elements.append(html.H5("Expected Impacts", className="mt-3"))
		elements.append(render_table(sorted_impact_names, [expected_impacts], table="expected"))

	if guaranteed_bounds:
		elements.append(html.H5("Guaranteed Bounds", className="mt-3"))
		elements.append(html.Div(
			render_table(
				sorted_impact_names,
				guaranteed_bounds,
				include_button=True,
				button_prefix="selected_bound",
				sort_by=sort_by,
				sort_order=sort_order,
				table="guaranteed"
			),
			id="guaranteed-table"
		))

	if possible_min_solution:
		elements.append(html.H5("Possible Min Bounds", className="mt-3"))
		elements.append(html.Div(
			render_table(
				sorted_impact_names,
				possible_min_solution,
				include_button=True,
				button_prefix="selected_bound",
				sort_by=sort_by,
				sort_order=sort_order,
				table="possible_min"
			),
			id="possible_min-table"
		))

	return html.Div(elements, className="p-3 sidebar-box")