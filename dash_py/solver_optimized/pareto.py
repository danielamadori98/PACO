import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from scipy.spatial import Delaunay

def get_pareto_frontier(frontier):
	pareto_frontier = []

	for i, arr in enumerate(frontier):
		dominated = False
		for j, other_arr in enumerate(frontier):
			if (i != j and # arr is_dominated by other_arr
				np.all(arr >= other_arr) and np.any(arr > other_arr)):
				dominated = True
				break
		if not dominated:
			# Check for duplicates
			if not any(np.array_equal(arr, x) for x in pareto_frontier):
				pareto_frontier.append(arr)

	return np.array(pareto_frontier)

def plot_pareto_frontier(pareto_frontier, all_points, impacts_names, file_name=""):
	num_dimensions = pareto_frontier.shape[1]

	if num_dimensions > 2:
		# Plot 3D for all triples of dimensions
		triples = list(combinations(range(num_dimensions), 3))
		for x_dim, y_dim, z_dim in triples:
			fig = plt.figure(figsize=(10, 8))
			ax = fig.add_subplot(111, projection='3d')

			ax.scatter(all_points[:, x_dim], all_points[:, y_dim], all_points[:, z_dim], label='All Points', color='blue')
			ax.scatter(pareto_frontier[:, x_dim], pareto_frontier[:, y_dim], pareto_frontier[:, z_dim], label='Pareto Frontier', color='red')

			# Create a Delaunay triangulation for the Pareto frontier
			tri = Delaunay(pareto_frontier[:, [x_dim, y_dim, z_dim]])
			ax.plot_trisurf(pareto_frontier[:, x_dim], pareto_frontier[:, y_dim], pareto_frontier[:, z_dim], triangles=tri.simplices, color='red', alpha=0.2)

			ax.set_xlabel(impacts_names[x_dim])
			ax.set_ylabel(impacts_names[y_dim])
			ax.set_zlabel(impacts_names[z_dim])
			ax.set_title(f'{impacts_names[x_dim]} vs {impacts_names[y_dim]} vs {impacts_names[z_dim]}')
			ax.legend()

			# Set the view angle
			ax.view_init(elev=45, azim=45)

			plt.tight_layout()
			if file_name != "":
				plt.savefig(f'{file_name}_3d_surface_{x_dim}_{y_dim}_{z_dim}.png')
			else:
				plt.show()# TODO: remove

	# Plot 2D for all pairs of dimensions
	pairs = list(combinations(range(num_dimensions), 2))
	num_pairs = len(pairs)

	# Calculate the size of the grid
	num_cols = int(np.ceil(np.sqrt(num_pairs)))
	num_rows = int(np.ceil(num_pairs / num_cols))

	fig, axes = plt.subplots(num_rows, num_cols, figsize=(20, 20))
	axes = axes.flatten()

	for ax, (x_dim, y_dim) in zip(axes, pairs):
		ax.scatter(all_points[:, x_dim], all_points[:, y_dim], label='All Points', color='blue')
		ax.scatter(pareto_frontier[:, x_dim], pareto_frontier[:, y_dim], label='Pareto Frontier', color='red')

		pareto_sorted = pareto_frontier[pareto_frontier[:, x_dim].argsort()]
		ax.plot(pareto_sorted[:, x_dim], pareto_sorted[:, y_dim], color='red')

		ax.set_xlabel(impacts_names[x_dim])
		ax.set_ylabel(impacts_names[y_dim])
		ax.set_title(f'{impacts_names[x_dim]} vs {impacts_names[y_dim]}')
		ax.legend()

	# Hide any unused subplots
	for ax in axes[num_pairs:]:
		fig.delaxes(ax)

	plt.tight_layout()
	if file_name != "":
		plt.savefig(f'{file_name}_2d.png')
	else:
		plt.show()


'''
TEST

# Generate more test points for 4 dimensions
np.random.seed(0)  # For reproducibility
more_frontier_points = [np.random.randint(1, 10, 4) for _ in range(10)]
more_failed_points = [np.random.randint(1, 10, 4) for _ in range(10)]

frontier_solution_value_bottom_up = [
	np.array([1, 2, 3, 4]), np.array([2, 3, 4, 5]), np.array([2, 1, 5, 6]),
	*more_frontier_points
]
failed_frontier_solution_value_bottom_up = [
	np.array([3, 2, 1, 7]), np.array([1, 1, 4, 8]), np.array([2, 2, 3, 9]),
	*more_failed_points
]
impacts_names = ["Impact 1", "Impact 2", "Impact 3", "Impact 4"]

combined_list = frontier_solution_value_bottom_up + failed_frontier_solution_value_bottom_up
pareto_frontier = get_pareto_frontier(combined_list)
all_points = np.array(combined_list)

# Example with specific angles
plot_pareto_frontier(pareto_frontier, all_points, impacts_names, file_name="pareto_frontier")
'''
