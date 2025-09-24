
from scripts.graph_traversals import get_largest_connected_component
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.path_constants import data_dir_path, project_root

def run_func_on_all_files(func, file_list:list):
    """Runs on all files in a single-threaded way"""
    result = []
    for file in file_list:
        print(f"------ Computing for file {file} ------")
        full_path = os.path.join(data_dir_path, file)
        graph = get_largest_connected_component(filename=full_path)
        print(f"Size of Largest Component: {len(graph.keys())}")
        result.append(func(graph))
    return result

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