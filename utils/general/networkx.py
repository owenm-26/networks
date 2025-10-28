import networkx as nx
from specific.florentine_families import create_florentine_adj_list
import matplotlib.pyplot as plt


def create_networkx_graph_from_adj_list(adj_list: dict):

    edge_list = []
    for node in adj_list:
        for edge in adj_list[node]:
            edge_list.append((node, edge))
    G = nx.Graph()
    G.add_edges_from(ebunch_to_add=edge_list)
    return G


if __name__ == "__main__":
    graph = create_networkx_graph_from_adj_list(adj_list=create_florentine_adj_list())
    plt.figure(figsize=(8, 6))
    nx.draw_networkx(graph, with_labels=True, node_color="lightblue", edge_color="gray")
    plt.title("Florentine Family Network")
    plt.show()

    