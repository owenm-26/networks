from convert import convert_data_to_adj_list, get_data_paths
from charts import create_scatter_plot
from collections import deque
import os
import pickle

def get_largest_connected_component(filename: str):
    """BFS that returns only the nodes in the largest connected component."""

    connected_components = []
    adj_list = convert_data_to_adj_list(filename=filename)
    seen = set()

    # print(f"Finished creating adj_list of {filename}. Starting BFS...")

    for key in adj_list.keys():
        if key not in seen:
            seen_nodes = bfs(graph=adj_list, start_node=key)
            connected_components.append(seen_nodes)
            seen.update(seen_nodes)

    # print(f"Finding the largest component out of {len(connected_components)}")
    largest_component_index = 0
    for i in range(1, len(connected_components)):
        if len(connected_components[i]) > len(connected_components[largest_component_index]):
            largest_component_index = i
    
    return adj_list, connected_components[largest_component_index]


def bfs(graph: dict, start_node: int):
    # print(f"Running BFS on node {start_node}")
    queue = deque()
    seen_nodes = set()
    
    seen_nodes.add(start_node)
    queue.append(start_node)
    
    while queue:
        current_node = queue.popleft()        
        for neighbor in graph.get(current_node, []):
            if neighbor not in seen_nodes:
                seen_nodes.add(neighbor)
                queue.append(neighbor)

    return seen_nodes


def average_number_of_friends(graph: dict):
    """Return the average number of friends per node."""
    total_friends = sum(len(neighbors) for neighbors in graph.values())
    total_nodes = len(graph)
    return total_friends / total_nodes if total_nodes > 0 else 0


def average_number_of_friends_friends(graph: dict):
    """Return the average number of friends-of-friends per node."""
    running_sum = 0
    total_nodes = len(graph)
    for neighbors in graph.values():
        if neighbors:  # avoid division by zero
            temp_sum = sum(len(graph[node]) for node in neighbors)
            running_sum += temp_sum / len(neighbors)
    return running_sum / total_nodes if total_nodes > 0 else 0

def get_friends_data_for_all_data(data_dir_path: str, data_paths: list):
    avg_friends = []
    avg_friends_of_friends = []
    names_of_schools = []
    

    for item_name in data_paths:
        full_path = os.path.join(data_dir_path, item_name)
        if os.path.isfile(full_path):
            print(f"--------- {item_name} ---------")
            adj_list, list_of_nodes = get_largest_connected_component(full_path)
            
            # Build a filtered adjacency list containing only nodes in the largest component
            narrowed_adj_list = {key: value for key, value in adj_list.items() if key in list_of_nodes}
            
            curr_avg_friends=average_number_of_friends(narrowed_adj_list)
            curr_avg_friends_of_friends = average_number_of_friends_friends(narrowed_adj_list)

            avg_friends.append(curr_avg_friends)
            avg_friends_of_friends.append(curr_avg_friends_of_friends)
            names_of_schools.append(item_name[:-3])

            print(f"Average friends: {curr_avg_friends}")
            print(f"Average friends-of-friends: {curr_avg_friends_of_friends}")
    
    return avg_friends, avg_friends_of_friends, names_of_schools

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sorted_dir_list=get_data_paths(project_root)

    # File to save results
    save_file = os.path.join(project_root, "friends_data.pkl")

    if os.path.exists(save_file):
        # Load precomputed data
        with open(save_file, "rb") as f:
            avg_friends, avg_friends_of_friends, names_of_schools = pickle.load(f)
        print("Loaded precomputed data.")
    else:
        # Compute the data
        avg_friends, avg_friends_of_friends, names_of_schools = get_friends_data_for_all_data(data_dir_path= os.path.join(project_root, "data"), data_paths=sorted_dir_list)

        # Save it for future use
        with open(save_file, "wb") as f:
            pickle.dump((avg_friends, avg_friends_of_friends, names_of_schools), f)
        print("Computed and saved data.")

    create_scatter_plot(x=avg_friends, 
                        y=avg_friends_of_friends, 
                        x_label="Average Number of Friends", 
                        y_label="Average Number of Friends of Friends", 
                        title="Question 2 (no labels)",
                        paradox_line=False)
    
    create_scatter_plot(x=avg_friends, 
                        y=avg_friends_of_friends, 
                        x_label="Average Number of Friends", 
                        y_label="Average Number of Friends of Friends", 
                        title="Question 2 (with labels)",
                        labels=names_of_schools,
                        paradox_line=False)



    
    

