from utils.general.convert_raw_data_to_adj import convert_raw_data_to_attributes, get_data_paths, adj_list_to_adj_matrix
import os
import networkx as nx
from utils.specific.node import Node
import enum
import time
import pickle

class Comparison(enum.Enum):
    GENDER="gender"
    STUDENT_STATUS="student_status"
    MAJOR = "major"
    DEGREE = "degree"

def compute_modularity(adj_list:dict, mx2:int, attributes_map: dict, comparison_mode: Comparison) -> list:
    """Computes modularity of"""
    # compute m as number of values/2
    print(f"- Computing {comparison_mode.value}")
    
    Q = 0
    for i, neighbors in adj_list.items():
        node_i = attributes_map[i]
        k_i = len(neighbors)
        for j in neighbors:
            node_j = attributes_map[j]
            k_j = len(adj_list[j])
            gamma = gamma_function(node_i, node_j, comparison_mode)
            Q += (1 - (k_i * k_j / mx2)) * gamma
    return Q / mx2

def gamma_function(node_i: Node,
                   node_j: Node,
                   comparison: Comparison) -> int:
    """Compares a variable attribute of Node in the modularity calculation"""
    same = False
    match comparison:
        case Comparison.GENDER:
            same = node_i.gender == node_j.gender
        
        case Comparison.STUDENT_STATUS:
            same = node_i.student_status == node_j.student_status

        case Comparison.MAJOR:
            same = node_i.major == node_j.major

        case Comparison.DEGREE:
            same = node_j.vertex_degree == node_j.vertex_degree
        
    return 1 if same else 0

def get_modularity_metrics_of_all_files(data_dir_path, file_list: list, run_limit:int = None) -> list:
    """Computes modularity metrics for all Comparisons across all files in filelist"""
    comparison_metrics = [Comparison.GENDER, Comparison.MAJOR, Comparison.STUDENT_STATUS, Comparison.DEGREE]
    gender_modularities, major_modularities, student_status_modularities, degree_modularities = [],[],[],[]
    modularities = [gender_modularities, major_modularities, student_status_modularities, degree_modularities]
    
    files_processed = 0
    for file in file_list:
        
        file_name = os.path.join(data_dir_path, file)
        start_time = time.perf_counter()

        # get input data
        attributes_map, adj_list = convert_raw_data_to_attributes(filename=file_name) 
        # adj_matrix, index_mapping = adj_list_to_adj_matrix(adj_list=adj_list)
        mx2 = 0
        for key in adj_list:
            mx2 += len(adj_list[key])
        print(f"--{file}({len(adj_list)} nodes, {int(mx2/2)} edges)--")
        # get each modularity metric
        for i in range(len(comparison_metrics)):
            measurement = compute_modularity(adj_list=adj_list, mx2=mx2, attributes_map=attributes_map, comparison_mode=comparison_metrics[i])
            modularities[i].append(measurement)

        end_time = time.perf_counter()
        print(f"(+) {file}: {end_time - start_time}s")
        files_processed+=1
        if run_limit and run_limit <= files_processed:
            break
    return modularities

import networkx as nx

def fast_modularity(adj_list, attributes_map, comparison_mode):
    G = nx.Graph()
    for node, neighbors in adj_list.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    # group nodes by attribute
    communities = {}
    for node, attr in attributes_map.items():
        key = getattr(attr, comparison_mode.value)
        communities.setdefault(key, set()).add(node)
    # compute modularity
    return nx.community.modularity(G, list(communities.values()))


if __name__ == "__main__":
    # example
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir_path= os.path.join(project_root, "data")
    # american = os.path.join(data_dir_path, get_data_paths(project_root)[1]) 

    # # get input data
    # attributes_map, adj_list = convert_raw_data_to_attributes(filename=american)    
    # gender_modularity = compute_modularity(adj_list=adj_list, attributes_map=attributes_map, comparison_mode=Comparison.GENDER)
    # print(f"gender_modularity: {gender_modularity}")

    save_file = os.path.join(project_root, "modularities.pkl")

    if os.path.exists(save_file):
        # Load precomputed data
        with open(save_file, "rb") as f:
            modularities = pickle.load(f)
        print("Loaded precomputed data.")
    else:
        modularities = get_modularity_metrics_of_all_files(data_dir_path=data_dir_path, file_list=get_data_paths(project_root=project_root), run_limit=None)
        with open(save_file, "wb") as f:
                pickle.dump(modularities, f)
        print("Computed and saved data.")
