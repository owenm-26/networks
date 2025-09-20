from convert import convert_data_to_adj_list, get_data_paths
from distance import get_diameter
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
data_dir_path= os.path.join(project_root, "data")

def run_func_on_all_files(func, file_list:list):
    result = []
    for file in file_list:
        full_path = os.path.join(data_dir_path, file)
        graph = convert_data_to_adj_list(filename=full_path)
        result.append(func(graph))
    return result

if __name__ == "__main__":
    sorted_dir_list=get_data_paths(project_root)[:2]
    result = run_func_on_all_files(get_diameter, sorted_dir_list)
    print(result)