import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community.centrality import girvan_newman

from plots import *
from metrics import *
from network_loader import NetworkLoader
from longitudinal import *

PATH = "./charliehebdo-all-rnr-threads/"


loader = NetworkLoader(PATH)


def main():
    G = loader.get_graph()
    print_general(G)
    degrees = print_degrees(G)
    centralities = print_centrality(G)
    clustering = print_clustering(G)
    components = print_components(G)
    density = print_density(G)
    plot_distributions(degrees, centralities, clustering)    
    print_communities(G)    
    show_plots(G)
    D = loader.get_graph(directed=True)
    network_activity(D)
    network_evolution()


"""
This function prints the network degrees, centralities, and clustering distributions
"""
def plot_distributions(degrees, centralities, clustering):
    degree_distribution(degrees)
    centrality_distribution(centralities)
    clustering_distribution(clustering)



# PART 2
def print_communities(G):
    max_clique = nx.graph_clique_number(G)
    print(f"Max clique = {max_clique}")

    cliques = list(nx.enumerate_all_cliques(G))
    number_of_cliques = [len(c) for c in cliques if len(c) >= 3]
    print(f"Number of cliques (>3) = {len(number_of_cliques)}")

    cross = 0
    for (n0, n1) in G.edges():
        if G.nodes[n0]['isSpreadingRumours'] ^ G.nodes[n1]['isSpreadingRumours']:
            cross += 1
    r = nr = 0
    for n in G.nodes():
        if G.nodes[n]['isSpreadingRumours']:
            r += 1
        else:
            nr += 1
    print(f"Homophily cross-(non)rumour = {cross / len(G.edges):.4f}")
    print(f'\t 2qp = {(2 * r * nr) / (len(G.nodes()) ** 2):.4f}')

    homophily = nx.numeric_assortativity_coefficient(G, 'isSpreadingRumours')
    print(f'homophily = {homophily}')

    bridges = nx.bridges(G)
    # look at bridges with high centarilty or something
    print(f'bridges = {len(list(bridges))}')

    """
    generater = girvan_newman(G)
    next(generater)
    print("Test")
    communities = [[G.nodes[n]['isSpreadingRumours'] for n in c] for c in next(generater)]
    print(f"number of communities = {len(communities)}")
    l = [c.count(True) / len(c) for c in communities]
    for i in range(5):
        print(f"{l[i]:2f}", end='')
    print()
    original_len = len(communities)
    while (len(communities) < 3 * original_len):
        communities = [[G.nodes[n]['isSpreadingRumours'] for n in c] for c in next(generater)] 
        l = [c.count(True) / len(c) for c in communities]
        print(f"number of communities = {len(communities)}")
        for i in range(5):
            print(f"{l[i]:2f}", end='')
        print()    
    """

    D = loader.get_graph(directed=True)
    hubs, authorities = nx.hits(D)

    global max_hub
    global max_authority

    max_hub = max(hubs, key=hubs.get)
    max_authority = max(authorities, key=authorities.get)

    print(f'Max hub node = {max_hub} with value of {hubs[max_hub]}')
    print(f'{D.nodes[max_hub]}')
    print(
        f'Max authority node = {max_authority} with value of {authorities[max_authority]}')
    print(f'{D.nodes[max_authority]}')

    print(f'partitioning')


def show_plots(G):
    markers = [plt.Line2D([0,0],[0,0], color='blue', marker='o', linestyle=''),
                plt.Line2D([0,0],[0,0], color='red', marker='o', linestyle='')]

    # Clique graph
    clique_G = G.subgraph(sorted([x for x in nx.find_cliques(G)], key=len)[-1])
    clique_color_map = ['blue' * G.nodes[n]['isSpreadingRumours'] + 'red' * (not G.nodes[n]['isSpreadingRumours']) for n in clique_G]
    clique_node_map = [100 * G.degree(n) for n in clique_G]
    nx.draw(clique_G, node_color=clique_color_map, node_size=clique_node_map)
    plt.legend(markers, ['Rumours', 'Non-Rumours'])
    plt.show()

    # Ego-Graph
    ego_hub = nx.ego_graph(G, max_hub)
    color_map = []
    node_map = []
    i = 0
    for node in ego_hub:
        if ego_hub.nodes[node]['isSpreadingRumours'] == True:
            color_map.append('blue')
        else:
            color_map.append('red')
        node_map.append(ego_hub.degree[node] * 100)
        i += 1
    nx.draw(ego_hub, node_color=color_map, node_size=node_map)
    plt.legend(markers, ['Rumours', 'Non-Rumours'])
    plt.show()
    ego_authority = nx.ego_graph(G, max_authority)
    authority_color_map = []
    authority_node_map = []
    i = 0
    for node in ego_authority:
        if ego_authority.nodes[node]['isSpreadingRumours'] == True:
            authority_color_map.append('blue')
        else:
            authority_color_map.append('red')
        authority_node_map.append(ego_authority.degree[node] * 5)
        i += 1
    nx.draw(ego_authority, node_size=authority_node_map,
            node_color=authority_color_map)
    plt.legend(markers, ['Rumours', 'Non-Rumours'])
    plt.show()


if __name__ == "__main__":
    main()
