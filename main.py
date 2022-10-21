from html import entities
from re import sub
import networkx as nx
import matplotlib.pyplot as plt
import network_loader as loader


PATH = "./charliehebdo-all-rnr-threads/"


def main():
    G = loader.load_rnr_graph(PATH)
    print_metrices(G)
    print_communities(G)


# PART 1
"""
This function prints the metrices of network
"""
def print_metrices(G):
    number_of_vertices = len(G.nodes)
    number_of_edges = len(G.edges)
    degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
    degree_max = max(degree_sequence)
    degree_min = min(degree_sequence)
    degree_avg = sum(degree_sequence) / len(degree_sequence)
    centrality = nx.degree_centrality(G)
    clustering_coef = nx.clustering(G)
    # network_diameter = nx.diameter(G) => ERROR inf length
    max_component = max(nx.connected_components(G), key=len)
    # network_diameter = nx.diameter(G.subgraph(max(nx.connected_components(G), key=len)))
    network_density = nx.density(G)
    number_component = len(list(nx.connected_components(G)))
    size_max_component = len(list(max_component))
    size_component = [len(list(n)) for n in nx.connected_components(G)]

    print(f"Number of Vertices = {number_of_vertices}")
    print(f"Number of Edges = {number_of_edges}")
    print(f"Degree Sequence = {degree_sequence[0:10]}")
    print(f"Degree Max = {degree_max}")
    print(f"Degree Min = {degree_min}")
    print(f"Degree Average = {degree_avg}")
    print(f"Centrality = {list(centrality.values())[0:10]}")
    print(f"Clustering Coefficient = {list(clustering_coef.values())[0:10]}")
    print(f"Density = {network_density}")
    print(f"Number of components = {number_component}")
    print(f"Maximum component = {size_max_component}")
    print(f"Component size = {size_component[0:9]}\n")


# PART 2
def print_communities(G):
    max_clique = nx.graph_clique_number(G)
    print(f"Max clique = {max_clique}")

    cliques = list(nx.enumerate_all_cliques(G))
    number_of_cliques = [len(c) for c in cliques if len(c) >= 3]
    print(f"Number of cliques (>3) = {len(number_of_cliques)}")


#print(G.nodes)
#print(G.edges)

#nx.draw(G)
#plt.show()

if __name__ == "__main__":
    main()