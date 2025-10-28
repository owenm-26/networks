
from graph_traversals import get_largest_connected_component
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from path_constants import data_dir_path, project_root
from concurrent.futures import ProcessPoolExecutor, as_completed


def run_func_on_all_files(func, file_list:list):
    """Runs on all files in a single-threaded way"""
    result = []
    for file in file_list:
        print(f"------ Computing for file {file} ------")
        full_path = os.path.join(data_dir_path, file)
        graph = get_largest_connected_component(filename=full_path)
        result.append(func(graph))
    return result

def run_func_on_all_files_distance(func, file_list:list):
    """Runs on all files in a single-threaded way"""
    diameters, avg_shortest_paths, largest_connected_components = [], [], []
    for file in file_list:
        print(f"------ Computing for file {file} ------")
        full_path = os.path.join(data_dir_path, file)
        graph = get_largest_connected_component(filename=full_path)
        G_diameter, G_avg_shortest_path, G_largest_connected_component = func(graph)
        diameters.append(G_diameter)
        avg_shortest_paths.append(G_avg_shortest_path)
        largest_connected_components.append(G_largest_connected_component)
    return diameters, avg_shortest_paths, largest_connected_components

def run_func_on_one_file(func, filename: str):
    """Process function for multi-threaded parent function"""
    print(f"------ Computing for file {filename} ------")
    full_path = os.path.join(data_dir_path, filename)
    # graph = convert_data_to_adj_list(filename=full_path)
    graph = get_largest_connected_component(filename=full_path)
    return func(graph)

def run_multithreaded_func_on_all_files(func, file_list:list, max_workers=5):
    """Runs on all files in a multi-threaded way"""
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(run_func_on_one_file, func, os.path.join(data_dir_path, file)): file for file in file_list}
        for future in as_completed(future_to_file):
            print("Thread completed.")
            results.append(future.result())
    return results

def run_multithreaded_func_on_all_files_distance(func, file_list: list, max_workers=5):
    """Runs func(graph) on all files in a multi-threaded way, 
    expecting func to return (diameter, avg_shortest_path, largest_connected_component)."""

    diameters, avg_shortest_paths, largest_connected_components = [], [], []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {
            executor.submit(
                run_func_on_one_file, func, os.path.join(data_dir_path, file)
            ): file
            for file in file_list
        }

        for future in as_completed(future_to_file):
            print(f"Thread completed for {future_to_file[future]}")
            G_diameter, G_avg_shortest_path, G_largest_connected_component = future.result()
            diameters.append(G_diameter)
            avg_shortest_paths.append(G_avg_shortest_path)
            largest_connected_components.append(G_largest_connected_component)

    return diameters, avg_shortest_paths, largest_connected_components

from concurrent.futures import ProcessPoolExecutor, as_completed
import os

def run_multiprocessing_func_on_all_files_distance(func, file_list: list, max_workers=8):
    """
    Runs func(graph) on all files in a multi-processing way,
    expecting func to return (diameter, avg_shortest_path, largest_connected_component).
    """

    diameters, avg_shortest_paths, largest_connected_components = [], [], []

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {
            executor.submit(
                run_func_on_one_file, func, os.path.join(data_dir_path, file)
            ): file
            for file in file_list
        }

        for future in as_completed(future_to_file):
            file = future_to_file[future]
            try:
                G_diameter, G_avg_shortest_path, G_largest_connected_component = future.result()
                diameters.append(G_diameter)
                avg_shortest_paths.append(G_avg_shortest_path)
                largest_connected_components.append(G_largest_connected_component)
                print(f"Process completed for {file}")
            except Exception as e:
                print(f"⚠️ Error in file {file}: {e}")

    return diameters, avg_shortest_paths, largest_connected_components

