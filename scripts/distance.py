from graph_traversals import bfs_distance_between_nodes
from convert import get_data_paths
from visualizations import create_scatter_plot
import os
import pickle
import time
from utils import run_multithreaded_func_on_all_files, project_root, data_dir_path

def get_distances_between_all_pairs_of_nodes(graph: dict):
    distances = []
    for starting_node in graph.keys():
        distances.extend(bfs_distance_between_nodes(graph=graph, starting_node=starting_node))
        print(f"Finished BFS for node {starting_node}.")
    return distances

def get_diameter(distances: list):
    return max(distances)

def get_average_shortest_path(distances: list):
    return sum(distances) / len(distances)

if __name__ == "__main__":
    start_time = time.perf_counter()
    sorted_dir_list=get_data_paths(project_root)[:12]

    save_file = os.path.join(project_root, "distance_and_path_data.pkl")

    if os.path.exists(save_file):
        with open(save_file, "rb") as f:
            diameters, avg_shortest_path_lengths, size_of_largest_components = pickle.load(f)
        print("Loaded precomputed data.")
    else:
        # results of BFS, input to the other functions
        distances = run_multithreaded_func_on_all_files(func=get_distances_between_all_pairs_of_nodes, file_list=sorted_dir_list)

        diameters = [get_diameter(distances=distance_list) for distance_list in distances]
        avg_shortest_path_lengths = [get_average_shortest_path(distances=distance_list) for distance_list in distances]
        size_of_largest_components = run_multithreaded_func_on_all_files(len, sorted_dir_list)

        with open(save_file, "wb") as f:
            pickle.dump((diameters, avg_shortest_path_lengths, size_of_largest_components), f)
        print("Computed and saved data.")
    
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"* Total Time Elapsed to go through {len(sorted_dir_list)} schools: {elapsed_time:.6f} seconds")

    # diameter d versus largest network component size
    create_scatter_plot(x=size_of_largest_components,
                        y=diameters,
                        x_label="Size of Largest Connected Components",
                        y_label="Diameters",
                        title="Q2.D Size of Largest Connected Components x Diameters",
                        )

    # length of shortest path avg versus largest network component size
    create_scatter_plot(x=size_of_largest_components,
                        y=avg_shortest_path_lengths,
                        x_label="Size of Largest Connected Components",
                        y_label="Average Shortest Path Lengths",
                        title="Q2.D Size of Largest Connected Components x Average Shortest Path Lengths",
                        )