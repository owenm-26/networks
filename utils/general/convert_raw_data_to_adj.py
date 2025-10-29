#!/usr/bin/python
import scipy
import scipy.io
import numpy as np
import os
from utils.general.path_constants import data_dir_path, project_root
from utils.specific.node import Node
import collections

def get_data_paths(project_root:str):
	data_dir = os.path.join(project_root, "data")
	sorted_dir_list = sorted(os.listdir(data_dir))
	return sorted_dir_list

def convert_data_to_adj_list(filename: str):
	# load the .mat file into a dictionary
	data = {}
	scipy.io.loadmat(filename, data)

	adj_list = {}

	# Find the adjacency matrix (A)
	A = data.get("A")
	if A is None:
		raise ValueError(f"No adjacency matrix 'A' found in the {filename} file.")


	# Convert A to COO format if it isn't already
	A = scipy.sparse.coo_matrix(A)

	# Build adjacency list
	adj_list = {}
	for i, j in zip(A.row, A.col):
		adj_list.setdefault(int(i), []).append(int(j))
		adj_list.setdefault(int(j), []).append(int(i))

	# (Optional) sort adjacency lists for consistency
	for k in adj_list:
		adj_list[k].sort()

	return adj_list

def convert_raw_data_to_attributes(filename: str):
    # Load .mat file
	data = scipy.io.loadmat(filename)

	# Extract adjacency matrix and local_info
	A = data.get("A")
	local_info = data.get("local_info")

	if A is None:
		raise ValueError(f"No adjacency matrix 'A' found in {filename}.")
	if local_info is None:
		raise ValueError(f"No 'local_info' found in {filename}.")

	# Convert to sparse COO format
	A = scipy.sparse.coo_matrix(A)

	# Build adjacency list
	adj_list = collections.defaultdict(set)
	for i, j in zip(A.row, A.col):
		if i != j:  # ignore self-loops
			adj_list[i].add(j)
			adj_list[j].add(i)

	# Build node attributes
	node_dict = {}
	for i in range(local_info.shape[0]):
		info = local_info[i]
		degree = len(adj_list[i])
		node = Node(
			student_status=info[0],
			gender=info[1],
			major=info[2],
			vertex_degree=degree
		)
		node_dict[i] = node
	
	return node_dict, adj_list

def adj_list_to_adj_matrix(adj_list:dict) -> list:
	n = len(adj_list)
	nodes = set(adj_list.keys())
	for neighbors in adj_list.values():
		nodes.update(neighbors)
    
    # Step 2: build mapping
	index_mapping = {node: idx for idx, node in enumerate(nodes)}
	n = len(nodes)
    
    # Step 3: build matrix
	matrix = [[0] * n for _ in range(n)]

	# Step 4: fill in edges
	for node, neighbors in adj_list.items():
		i = index_mapping[node]
		for neighbor in neighbors:
			j = index_mapping[neighbor]
			matrix[i][j] = 1
			matrix[j][i] = 1  # if undirected

	return matrix, index_mapping

    
if __name__ == "__main__":
	project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
	data_dir_path= os.path.join(project_root, "data")
	american = os.path.join(data_dir_path, get_data_paths(project_root)[1]) 
	adj = convert_data_to_adj_list(american)
	attr, adj_list = convert_raw_data_to_attributes(american)
	# print(adj)
	print(attr)
	# adj_list_to_adj_matrix(adj_list=adj_list)
