"""
This file is for print and calculating network metrics.
"""

import networkx as nx

MAX_LEN_PRINT = 5


"""
This function prints general information about a network (G)
"""
def print_general(G):
    print("Network general metrics:")
    print(f"node count = {len(G.nodes)} \nedge count = {len(G.edges)}\n")


"""
This function prints information about the degrees in a network (G)
"""
def print_degrees(G):
    print("Network degree metrics:")
    degrees = sorted((d for n, d in G.degree()), reverse=True)
    print(f"max degree = {degrees[0]} \nmin degree = {degrees[-1]}")
    print(f"avg degree = {sum(degrees) / len(degrees):.2f}\n")
    return degrees


"""
This function prints information about the centrality of a network (G)
"""
def print_centrality(G):
    print("Network centrality metrics:")
    centralities = nx.degree_centrality(G)
    values = list(centralities.values())
    print(f"avg node centrality = {sum(values)/len(values):.5f}")
    print(f"Top {MAX_LEN_PRINT} nodes in Degree Centrality")
    for node in sorted(centralities.keys(), key=lambda x: centralities[x], reverse=True)[:MAX_LEN_PRINT]:
        print(f"\tnode({node}) = {centralities[node]:.5f}")
    print() # print a newline
    return centralities


"""
This function prints information about the clustering coef of a network (G)
"""
def print_clustering(G):
    print("Network Clustering metrics:")
    clustering_coefs = nx.clustering(G)
    values = list(clustering_coefs.values())
    print(f"avg node clustering = {sum(values)/len(values):.5f}")
    print(f"Top {MAX_LEN_PRINT} nodes in Clustering coefficient")
    for node in sorted(clustering_coefs.keys(), key=lambda x: clustering_coefs[x], reverse=True)[:MAX_LEN_PRINT]:
        print(f"\tnode({node}) = {clustering_coefs[node]:.5f}")
    print() # print a newline
    return clustering_coefs


"""
This function prints information about the different connect components of the network (G)
"""
def print_components(G):
    print("Network Connected Components metrics:")
    components = sorted(list(nx.connected_components(G)), key=len, reverse=True)
    print(f"number of connected components = {len(components)}")
    component_sizes = [len(list(n)) for n in components]
    print(f"avg connected components size = {sum(component_sizes) / len(component_sizes):.2f}")
    print(f"Largest {MAX_LEN_PRINT} connected components")
    for i in range(MAX_LEN_PRINT):
        print(f"\tcomponent ({i}) size = {component_sizes[i]}")
    print() # print a newline
    return components


def print_diameter(G):
    # network_diameter = nx.diameter(G) => ERROR inf length
    # network_diameter = nx.diameter(G.subgraph(max(nx.connected_components(G), key=len)))
    raise NotImplemented

"""
This function prints information about the density of a network (G)
"""
def print_density(G):
    print("Network Density metrics:")
    network_density = nx.density(G)
    print(f"density = {network_density:.6f}\n")
    return network_density