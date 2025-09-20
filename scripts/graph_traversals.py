from collections import deque
from convert import convert_data_to_adj_list

def bfs_connected_components(graph: dict, start_node: int):
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

def get_largest_connected_component(filename: str):
    """BFS that returns only the nodes in the largest connected component."""

    connected_components = []
    adj_list = convert_data_to_adj_list(filename=filename)
    seen = set()

    # print(f"Finished creating adj_list of {filename}. Starting BFS...")

    for key in adj_list.keys():
        if key not in seen:
            seen_nodes = bfs_connected_components(graph=adj_list, start_node=key)
            connected_components.append(seen_nodes)
            seen.update(seen_nodes)

    # print(f"Finding the largest component out of {len(connected_components)}")
    largest_component_index = 0
    for i in range(1, len(connected_components)):
        if len(connected_components[i]) > len(connected_components[largest_component_index]):
            largest_component_index = i

    narrowed_adj_list = {key: value for key, value in adj_list.items() if key in connected_components[largest_component_index]}
    
    return narrowed_adj_list

def bfs_distance_between_nodes(graph: dict, starting_node: int):
    queue = deque()
    seen_nodes = set()

    queue.append(starting_node)
    seen_nodes.add(starting_node)

    distances = []
    level = 1

    while queue:
        current_node = queue.popleft()
        for neighbor in graph.get(current_node, []):
            if neighbor not in seen_nodes:
                seen_nodes.add(neighbor)
                queue.append(neighbor)
                distances.append(level)
        level +=1
    
    return distances