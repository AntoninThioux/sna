"""
This file contains the logic for loading the raw data in networkx graphs
"""

import networkx as nx
import json
import os
from dateutil import parser

PATH = "./charliehebdo-all-rnr-threads/"


def main():
    print('Trying to load graph...')
    G = load_rnr_graph(PATH)
    print('Rumours/non-rumour graph loaded successfully!')
    i = 0
    for n0, n1 in G.edges:
        if i > 20:
            break
        print(G[n0][n1])
        i += 1


"""
This function loads a single annotated tweet in the dataset.
"""
def load_tweet(tid, G, path):
    f = open(path + f'{tid}/source-tweets/{tid}.json')
    tweet = json.load(f)
    f.close()

    G.add_node(tweet['user']['id'])
    G.add_edges_from([(tweet['user']['id'], m['id']) for m in tweet['entities']['user_mentions']])
    set_edge_time(G, tweet)

    return tweet['user']['id']


def load_tweet_annotations(tid, G, path, nid):
    f = open(path + f'{tid}/annotation.json')
    annotation = json.load(f)
    f.close()

    if (annotation['is_rumour'] == 'rumour'):
        G.nodes[nid]['rumour_count'] = G.nodes[nid].get('rumour_count', 0) + 1
    else:
        G.nodes[nid]['non-rumour_count'] = G.nodes[nid].get('non-rumour_count', 0) + 1


"""
This function loads the reactions to a tweet in the dataset.
"""
def load_reactions(tid, G, path):
    r_ids = []
    
    for reaction_file in os.listdir(path + f'{tid}/reactions'):
        rf = open(path + f'{tid}/reactions/' + reaction_file)
        subtweet = json.load(rf)
        rf.close()

        G.add_edges_from([(subtweet['user']['id'], m['id']) for m in subtweet['entities']['user_mentions']])
        set_edge_time(G, subtweet)

        r_ids.append(subtweet['user']['id']) 

    return r_ids


def guilt_by_reaction(tid, G, path, rn_ids):
    f = open(path + f'{tid}/annotation.json')
    annotation = json.load(f)
    f.close()

    for rid in rn_ids:
        if (annotation['is_rumour'] == 'rumour'):
            G.nodes[rid]['rumour_count'] = G.nodes[rid].get('rumour_count', 0) + 1
        else:
            G.nodes[rid]['non-rumour_count'] = G.nodes[rid].get('non-rumour_count', 0) + 1


"""
This function sets the time attribute to the edges in the graph.
"""
def set_edge_time(G, tweet_json):
    for m in tweet_json['entities']['user_mentions']:
        edge = G[tweet_json['user']['id']][m['id']]
        if 'times' not in edge.keys():
            edge['times'] = []

        edge['times'].append(parser.parse(tweet_json['created_at'])) 

    
"""
This function loads the tweets in a directory.
"""
def load_directory(G, dir):
    x = 0

    ids = os.listdir(dir)
    for tweet_id in ids:
        node_id = load_tweet(tweet_id, G, dir)
        rnode_ids = load_reactions(tweet_id, G, dir)
        load_tweet_annotations(tweet_id, G, dir, node_id)
        guilt_by_reaction(tweet_id, G, dir, rnode_ids)
        x += 1
        print(f'\rLoaded {x / len(ids) * 100:.1f}% tweets from {dir}',end="")
    
    print(f'\rLoaded 100.0% of tweets from {dir}')


"""
This function classifies all nodes in the graph as rumour-spreaders and non-rumour-spreaders
"""
def classify(G):
    for n in G.nodes:
        rc = G.nodes[n].get('rumour_count', 0)
        nrc = G.nodes[n].get('non-rumour_count', 0)
        G.nodes[n]['is_spreading_rumours'] = (rc > nrc)
        
    
"""
This function loads the graph.
"""
def load_rnr_graph(path, directed=False):
    G = None

    if (directed):
        G = nx.DiGraph()
    else:
        G = nx.Graph()

    load_directory(G, path + "rumours/")
    load_directory(G, path + "non-rumours/")
    classify(G)
    return G


if __name__ == "__main__":
    main()