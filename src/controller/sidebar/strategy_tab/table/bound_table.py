
import dash
from dash import Input, Output, State, ALL, ctx
from env import IMPACTS_NAMES, BOUND
from view.sidebar.strategy_tab.table.bound_table import get_bound_table


def sync_bound_store_from_bpmn(bpmn_store, bound_store):
	for name in sorted(bpmn_store[IMPACTS_NAMES]):
		print("sync_bound_store_from_bpmn: bpmn_store:impacts_names:", name)
		if name not in bound_store[BOUND]:
			bound_store[BOUND][name] = 1.0

	return bound_store


def register_bound_callbacks(bound_callbacks):
	@bound_callbacks(
		Output("bound-table", "children"),
		Input("bound-store", "data"),
		State("bpmn-store", "data"),
		prevent_initial_call=True
	)
	def regenerate_bound_table(bound_store, bpmn_store):
		if not bpmn_store or not bound_store or BOUND not in bound_store:
			raise dash.exceptions.PreventUpdate

		print("regenerate_bound_table", bound_store[BOUND])
		return get_bound_table(bound_store, sorted(bpmn_store[IMPACTS_NAMES]))


	@bound_callbacks(
		Output('bound-store', 'data', allow_duplicate=True),
		Input({'type': 'bound-input', 'index': ALL}, 'value'),
		State({'type': 'bound-input', 'index': ALL}, 'id'),
		State('bound-store', 'data'),
		prevent_initial_call='initial_duplicate'
	)
	def update_bounds(values, ids, bound_store):
		for value, id_obj in zip(values, ids):
			print("must be a name:", id_obj["index"])
			bound_store[id_obj["index"]] = float(value)

		print("update_bounds", bound_store[BOUND])
		return bound_store

	@bound_callbacks(
		Output("bound-store", "data", allow_duplicate=True),
		Input({"type": "selected_bound", "index": ALL, "table": ALL}, "n_clicks"),
		State("sort_store_guaranteed", "data"),
		State("sort_store_possible_min", "data"),
		State("bound-store", "data"),
		State("bpmn-store", "data"),
		prevent_initial_call=True
	)
	def update_bound_from_select(_, store_guaranteed, store_possible, bound_store, bpmn_store):
		trigger = ctx.triggered_id
		if not trigger:
			raise dash.exceptions.PreventUpdate

		selected_table = trigger["table"]
		selected_index = trigger["index"]

		selected_store = store_guaranteed if selected_table == "guaranteed" else store_possible
		selected_bound = selected_store["data"][selected_index]
		print("before:update_bound_from_select", bound_store[BOUND])
		for name, value in zip(sorted(bpmn_store[IMPACTS_NAMES]), selected_bound):
			bound_store[BOUND][name] = float(value)
		print("after:update_bound_from_select", bound_store[BOUND])
		return bound_store
