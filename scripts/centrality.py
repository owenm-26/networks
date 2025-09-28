from utils.florentine_families import create_florentine_adj_list
from utils.graph_traversals import bfs_distance_between_nodes, bfs_shortest_paths
import networkx as nx
from utils.networkx import create_networkx_graph_from_adj_list

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
    G = create_networkx_graph_from_adj_list(adj_list=graph)
    return nx.betweenness_centrality(G=G, normalized=True)

    # get the shortest paths from each node to every other node
    # all_shortest_paths = []
    # seen_paths = set()
    # for node in graph.keys():
    #     shortest_paths, new_paths = bfs_shortest_paths(graph=graph, start_node=node, master_seen_paths=seen_paths, master_betweenness_counts={})
    #     seen_paths.update(new_paths)
    #     all_shortest_paths.append(shortest_paths)

    # print(f"Seen Paths: {seen_paths}")
    # # count the number of times each node is between a path
    # divisor = 0
    # node_betweenness_counts = {node: 0 for node in graph.keys()}
    # for path in all_shortest_paths:
    #     for node_count in path:
    #         divisor +=1
    #         node_betweenness_counts[node_count] += path[node_count]
   
    # n = len(graph)
    # divisor = (n-1)*(n-2)/2
    # betweenness_centralities = [node_betweenness_counts[node]/divisor for node in node_betweenness_counts]
    
    # G = create_networkx_graph_from_adj_list(adj_list=graph)
    # print("NX:", nx.betweenness_centrality(G=G, normalized=True), "\n")
    # print("MY:", {key: value / divisor for key, value in node_betweenness_counts.items()})
    # return betweenness_centralities

def get_all_pagerank_centralities(graph: dict, alpha: float = 1.2) -> list:
    return []
    

if __name__ == "__main__":
    florentine_family_graph = create_florentine_adj_list()
    fake_graph = {"A": {"B","C"},
                    "B": {"A", "C", "E"},
                    "C": {"A","B","D"},
                    "D": {"C"},
                    "E": {"B"}
        }
    
    small_fake_graph = {"A": {"B"},
                        "B": {"A", "C"},
                        "C": {"B", "D"},
                        "D": {"C"}}

    degree_centralities = get_all_degree_centralities(graph=florentine_family_graph)
    closeness_centralities = get_all_closeness_centralities(graph=florentine_family_graph)
    betweenness_centralities = get_all_betweenness_centralities(graph=florentine_family_graph)

    print(f"Degree Centralities: {degree_centralities}")
    print(f"Closeness Centralities: {closeness_centralities}")
    print(f"Betweenness Centralities: {betweenness_centralities}")

    
