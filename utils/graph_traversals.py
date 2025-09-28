from collections import deque
from utils.convert import convert_data_to_adj_list

def bfs_shortest_paths(graph:dict, start_node: str, master_seen_paths: set, master_betweenness_counts: dict):

    def order_path_tuple(node1, node2) -> tuple:
        tup = ()
        if node1 > node2:
            tup = (node2, node1)
        else:
            tup = (node1, node2)
        return tup
    
    def all_betweenness_counts_on_path(start_node, end_node, seen_paths: set, parents: dict, betweenness_counts:dict):
        # print(f"Betweenness for {start_node} -> {end_node}")
        # print(f"SEEN PATHS: {seen_paths}")
        runner = parents[end_node]

        while runner != start_node:
            if order_path_tuple(start_node, end_node) not in seen_paths:
                # print(f"-Adding new betweenness: {runner}")
                betweenness_counts[runner] = 1 if runner not in betweenness_counts else betweenness_counts[runner] + 1
            else:
                # print(f"-Already in seeen: {start_node} -> {end_node}")
                break
            runner = parents[runner]
        
        return betweenness_counts
    
    queue = deque()
    seen_nodes = set()
    seen_paths = master_seen_paths
    parents = {}
    betweenness_counts = master_betweenness_counts
    seen_nodes.add(start_node)
    queue.append(start_node)
    parents[start_node] = None
    # print(f"Run {start_node}")
    while queue:
        current_node = queue.popleft()    
        for neighbor in graph.get(current_node, []):
            if neighbor not in seen_nodes:
                seen_nodes.add(neighbor)
                queue.append(neighbor)
                parents[neighbor] = current_node
                # Make sure that you don't add the start / end verticies to the path
                if start_node != current_node and order_path_tuple(neighbor, start_node) not in seen_paths:
                    betweenness_counts = all_betweenness_counts_on_path(start_node=start_node, end_node=neighbor, parents=parents, seen_paths=seen_paths, betweenness_counts=master_betweenness_counts)
                    new_paths = {order_path_tuple(start_node, neighbor), order_path_tuple(current_node, neighbor)}
                    seen_paths.update(new_paths)
                    # print(f"Found a new shortest path from {start_node} -> {neighbor}: {master_betweenness_counts}")
                elif start_node == current_node:
                    # print(f"{start_node} Path too short", end=": ")
                    seen_paths.add(order_path_tuple(current_node, neighbor))
                    # print(start_node, neighbor)
                else:
                    pass
                    # print("Already seen path", end=": ")
                    # print(start_node, neighbor, seen_paths)
            # print(f"Paths explored: {seen_paths}")
                    
    # Add all betweenness counts
    # print(f"Betweenness to be returned {betweenness_counts}")
    return betweenness_counts, seen_paths

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

def floyd_warshall(graph: dict):
    nodes = list(graph.keys())
    n = len(nodes)
    
    # Map node labels to 0..n-1 indices
    node_to_idx = {node: i for i, node in enumerate(nodes)}
    
    # Initialize distance matrix with +∞ (not -∞!)
    dist = [[float("inf") for _ in range(n)] for _ in range(n)]
    
    # Distance to neighbors is 1
    for node, neighbors in graph.items():
        i = node_to_idx[node]
        for neighbor in neighbors:
            j = node_to_idx[neighbor]
            dist[i][j] = 1
    
    # Distance to self is 0
    for i in range(n):
        dist[i][i] = 0
    
    # Floyd-Warshall relaxation
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    # Flatten distances into a single list
    distances = []
    for row in dist:
        distances.extend(row)
    
    return distances
