from html import entities
from re import sub
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import network_loader as loader
from networkx.algorithms.community.centrality import girvan_newman


PATH = "./charliehebdo-all-rnr-threads/"


def main():
    G = loader.load_rnr_graph(PATH)
    # print_metrices(G)
    # print_communities(G)
    show_plots(G)


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

    cross = 0
    for (n0, n1) in G.edges():
        if G.nodes[n0]['is_spreading_rumours'] and not G.nodes[n1]['is_spreading_rumours']:
            cross += 1
    r = nr = 0
    for n in G.nodes():
        if G.nodes[n]['is_spreading_rumours']:
            r += 1
        else:
            nr += 1
    print(f"Homophily cross-(non)rumour = {cross / len(G.edges):.4f}")
    print(f'\t 2qp = {r * nr / len(G.nodes()) / len(G.nodes()):.4f}')
        

    homophily = nx.numeric_assortativity_coefficient(G, 'is_spreading_rumours')
    print(f'homophily = {homophily}')

    bridges = nx.bridges(G)
    # look at bridges with high centarilty or something
    print(f'bridges = {len(list(bridges))}')

    """
    generater = girvan_newman(G)
    next(generater)
    print("Test")
    communities = [[G.nodes[n]['is_spreading_rumours'] for n in c] for c in next(generater)]
    print(f"number of communities = {len(communities)}")
    l = [c.count(True) / len(c) for c in communities]
    for i in range(5):
        print(f"{l[i]:2f}", end='')
    print()
    original_len = len(communities)
    while (len(communities) < 3 * original_len):
        communities = [[G.nodes[n]['is_spreading_rumours'] for n in c] for c in next(generater)] 
        l = [c.count(True) / len(c) for c in communities]
        print(f"number of communities = {len(communities)}")
        for i in range(5):
            print(f"{l[i]:2f}", end='')
        print()    
    """

    D = loader.load_rnr_graph_directed(PATH)
    hubs, authorities = nx.hits(D)

    max_hub = max(hubs, key=hubs.get)
    max_authority = max(authorities, key=authorities.get)

    print(f'Max hub node = {max_hub} with value of {hubs[max_hub]}')
    print(f'{D.nodes[max_hub]}')
    print(f'Max authority node = {max_authority} with value of {authorities[max_authority]}')
    print(f'{D.nodes[max_authority]}')

    print(f'partitioning')
    

def show_plots(G):
    # Degree distribution 
    degrees = [d for n,d in G.degree()]
    plt.hist(degrees)
    plt.yscale('log')
    plt.xscale()
    plt.show()
    
    # Centrality distribution
    number_of_points = nx.number_of_nodes(G)
    



#print(G.nodes)
#print(G.edges)

#nx.draw(G)
#plt.show()

if __name__ == "__main__":
    main()