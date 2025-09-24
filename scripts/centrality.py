from utils.florentine_families import create_florentine_adj_list
from utils.graph_traversals import bfs_distance_between_nodes

def get_all_degree_centralities(graph: dict) -> list:
    degree_centralities = []
    for node in graph.keys():
        degree_centralities.append(len(graph[node]))
    return degree_centralities

def get_all_closeness_centralities(graph:dict) -> list:
    closeness_centralities = []
    for node in graph.keys():
        distances = bfs_distance_between_nodes(graph=graph, starting_node=node)
        if len(distances) == 0:
            closeness_centralities.append(0)
        else:
            closeness_centralities.append(sum(distances)/len(distances))
    return closeness_centralities

def get_all_betweenness_centralities(graph: dict) -> list:
    return []

def get_all_pagerank_centralities(graph: dict, alpha: float = 1.2) -> list:
    return []
    

if __name__ == "__main__":
    florentine_family_graph = create_florentine_adj_list()

    degree_centralities = get_all_degree_centralities(graph=florentine_family_graph)
    closeness_centralities = get_all_closeness_centralities(graph=florentine_family_graph)
    print(f"Degree Centralities: {degree_centralities}")
    print(f"Closeness Centralities: {closeness_centralities}")