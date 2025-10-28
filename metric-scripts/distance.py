from utils.general.graph_traversals import bfs_distance_between_nodes
from utils.general.convert_raw_data_to_adj import get_data_paths
from utils.general.visualizations import create_scatter_plot
import os
import pickle
import time
from utils.general.multithreading import run_multithreaded_func_on_all_files, run_func_on_all_files, run_multiprocessing_func_on_all_files_distance
from utils.general.path_constants import data_dir_path, project_root
from networkx import average_shortest_path_length, diameter, connected_components
from utils.general.networkx import create_networkx_graph_from_adj_list

def get_distances_between_all_pairs_of_nodes(graph: dict):
    distances = []
    for starting_node in graph.keys():
        distances.extend(bfs_distance_between_nodes(graph=graph, starting_node=starting_node))
        print(f"Finished BFS for node {starting_node}.")
    return distances

def get_diameter(networkx_graph):
    return diameter(G=networkx_graph)

def get_average_shortest_path(networkx_graph):
    return average_shortest_path_length(G=networkx_graph)

def compute_for_one_school(graph:dict):
    start_time = time.perf_counter()
    G_largest_connected_component = len(graph.keys())
    print(f"-Largest component done: {G_largest_connected_component}")
    G = create_networkx_graph_from_adj_list(graph)
    G_diameter = diameter(G=G)
    print(f"-Diameter done")
    G_avg_shortest_path = average_shortest_path_length(G=G)
    print(f"-Avg shortest path done")
    end_time = time.perf_counter()
    elapsed_time = end_time- start_time
    print(f"Time taken for {G_largest_connected_component} nodes: {elapsed_time:.6f} seconds")

    return G_diameter, G_avg_shortest_path, G_largest_connected_component

if __name__ == "__main__":
    start_time = time.perf_counter()
    sorted_dir_list=get_data_paths(project_root)

    save_file = os.path.join(project_root, "distance_and_path_data.pkl")

    if os.path.exists(save_file):
        with open(save_file, "rb") as f:
            diameters, avg_shortest_paths, largest_connected_components = pickle.load(f)
        print("Loaded precomputed data.")
    else:
        diameters, avg_shortest_paths, largest_connected_components = run_multiprocessing_func_on_all_files_distance(func=compute_for_one_school, file_list=sorted_dir_list)

        with open(save_file, "wb") as f:
            pickle.dump((diameters, avg_shortest_paths, largest_connected_components), f)
        print("Computed and saved data.")
    
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"* Total Time Elapsed to go through {len(sorted_dir_list)} schools: {elapsed_time:.6f} seconds")

    # diameter d versus largest network component size
    create_scatter_plot(x=largest_connected_components,
                        y=diameters,
                        x_label="Size of Largest Connected Components",
                        y_label="Diameters",
                        title="Q2.D Size of Largest Connected Components x Diameters",
                        )

    # length of shortest path avg versus largest network component size
    create_scatter_plot(x=largest_connected_components,
                        y=avg_shortest_paths,
                        x_label="Size of Largest Connected Components",
                        y_label="Average Shortest Path Lengths",
                        title="Q2.D Size of Largest Connected Components x Average Shortest Path Lengths",
                        )