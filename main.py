from html import entities
from re import sub
import networkx as nx
import json
import matplotlib.pyplot as plt
import os

PATH = "./charliehebdo-all-rnr-threads/"

G = nx.Graph()

def load_tweet(tid, G, path):
    # Load main tweet
    f = open(path + f'{tid}/source-tweets/{tid}.json')
    tweet = json.load(f)
    f.close()

    for mention in tweet['entities']['user_mentions']:
        G.add_edge(tweet['user']['id'], mention['id'])

    # Load reactions
    files = os.listdir(path + f'{tid}/reactions')
    for reaction_file in files:
        if not reaction_file[0] == '.':
            rf = open(path + f'{tid}/reactions/' + reaction_file)
            subtweet = json.load(rf)
            G.add_edges_from([(subtweet['user']['id'], mention['id']) for mention in subtweet['entities']['user_mentions']])
                
            rf.close()


for tweet_id in os.listdir(PATH + '/rumours/'):
    if not tweet_id[0] == ".":
        #print(f"loading tweet: {tweet_id}...", end="")
        load_tweet(tweet_id, G, PATH + '/rumours/')
        #print("\tdone.")

for tweet_id in os.listdir(PATH + '/non-rumours/'):
    if not tweet_id[0] == ".":
        #print(f"loading tweet: {tweet_id}...", end="")
        load_tweet(tweet_id, G, PATH + '/non-rumours/')
        #print("\tdone.")


# PART 1

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
print(f"Component size = {size_component[0:9]}")


# PART 2
max_clique = nx.graph_clique_number(G)
print(f"Max clique = {max_clique}")

cliques = list(nx.enumerate_all_cliques(G))
number_of_cliques = [len(c) for c in cliques if len(c) >= 3]
print(f"Number of cliques (>3) = {len(number_of_cliques)}")


#print(G.nodes)
#print(G.edges)

#nx.draw(G)
#plt.show()

