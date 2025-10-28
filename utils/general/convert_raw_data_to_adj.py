#!/usr/bin/python
import scipy
import scipy.io
import numpy as np
import os
from path_constants import data_dir_path, project_root


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

if __name__ == "__main__":
	project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
	data_dir_path= os.path.join(project_root, "data")
	american = os.path.join(data_dir_path, get_data_paths(project_root)[1]) 
	print(american)
	print(len(convert_data_to_adj_list(american)))