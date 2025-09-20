from convert import  get_data_paths
from visualizations import create_scatter_plot
from graph_traversals import get_largest_connected_component
import os
import pickle

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
            narrowed_adj_list = get_largest_connected_component(full_path)
            
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



    
    

