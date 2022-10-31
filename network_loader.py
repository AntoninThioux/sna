"""
This file contains the logic for loading the raw data in networkx graphs
"""

import networkx as nx
import json
import os
from dateutil import parser
import datetime

PATH = "./charliehebdo-all-rnr-threads/"


def main():
    print('Trying to load graph...')
    loader = NetworkLoader()
    G = loader.get_graph(True)
    print('Rumours/non-rumour graph loaded successfully!')
    i = 0
    for n0, n1 in G.edges:
        if i > 20:
            break
        print(G[n0][n1])
        i += 1


"""
This is a class for loading Network graphs. 
It's main purpose is to cache the graphs so they can be retrieved without reloading.
"""
class NetworkLoader:
    """
    This method initializes the network loader
    """
    def __init__(self, path=PATH):
        self.G = None
        self.D = None
        self.path = path

    """
    Getter for the loaded graph objects
    """
    def get_graph(self, directed=False):
        if directed and self.D:
            return self.D
        elif not directed and self.G:
            return self.G

        if not directed and '.undirected.gml' in os.listdir('.'):
            x = None
            while (not x or x not in "NnYy01"):
                x = input('Use found cached file (.undirected.gml)? (Y/n): ')
            if (x in "Yy1"):
                self.G = nx.read_gml('.undirected.gml', destringizer=destringizer)
                return self.G
            
        elif directed and '.directed.gml' in os.listdir('.'):
            x = None
            while (not x or x not in "NnYy01"):
                x = input('Use found cached file (.directed.gml)? (Y/n): ')
            if (x in "Yy1"):
                self.D = nx.read_gml('.directed.gml', destringizer=destringizer)
                return self.D

        return self.load_rnr_graph(self.path, directed)

    """
    This function loads the graph.
    """
    def load_rnr_graph(self, path, directed=False):
        if (directed):
            self.D = nx.DiGraph()
            print("Loading Directed graph:")
            self._load_directory(self.D, path + "rumours/")
            self._load_directory(self.D, path + "non-rumours/")
            self._classify(self.D)
            nx.write_gml(self.D, ".directed.gml", stringizer=stringizer)
            return self.D
        else:
            self.G = nx.Graph()
            print("Loading Undirected graph:")
            self._load_directory(self.G, path + "rumours/")
            self._load_directory(self.G, path + "non-rumours/")
            self._classify(self.G)
            nx.write_gml(self.G, ".undirected.gml", stringizer=stringizer)
            return self.G

    """
    This method loads a single annotated tweet in the dataset.
    """
    def _load_tweet(self, tid, G, dir):
        f = open(dir + f'{tid}/source-tweets/{tid}.json')
        tweet = json.load(f)
        f.close()

        G.add_node(tweet['user']['id'])
        G.add_edges_from([(tweet['user']['id'], mention['id'])
                        for mention in tweet['entities']['user_mentions']])
        return tweet['user']['id']

    def _load_tweet_annotations(self, tid, G, dir, nid):
        f = open(dir + f'{tid}/annotation.json')
        annotation = json.load(f)
        f.close()

        if (annotation['is_rumour'] == 'rumour'):
            G.nodes[nid]['rumourCount'] = G.nodes[nid].get('rumourCount', 0) + 1
        else:
            G.nodes[nid]['nonRumourCount'] = G.nodes[nid].get('nonRumourCount', 0) + 1

    """
    This function loads the reactions to a tweet in the dataset.
    """
    def _load_reactions(self, tid, G, dir):
        r_ids = []
        if os.path.isdir(dir + f'{tid}/reactions'):
            files = os.listdir(dir + f'{tid}/reactions')
            for reaction_file in files:
                rf = open(dir + f'{tid}/reactions/' + reaction_file)
                subtweet = json.load(rf)
                rf.close()

                G.add_edges_from([(subtweet['user']['id'], mention['id'])
                                for mention in subtweet['entities']['user_mentions']])
                self._set_edge_time(G, subtweet)

                r_ids.append(subtweet['user']['id'])

        return r_ids

    def _guilt_by_reaction(self, tid, G, dir, rn_ids):
        f = open(dir + f'{tid}/annotation.json')
        annotation = json.load(f)
        f.close()

        for rid in rn_ids:
            if (annotation['is_rumour'] == 'rumour'):
                G.nodes[rid]['rumourCount'] = G.nodes[rid].get(
                    'rumourCount', 0) + 1
            else:
                G.nodes[rid]['nonRumourCount'] = G.nodes[rid].get(
                    'nonRumourCount', 0) + 1

    """
    This function sets the time attribute to the edges in the graph.
    """
    def _set_edge_time(self, G, tweet_json):
        for m in tweet_json['entities']['user_mentions']:
            edge = G[tweet_json['user']['id']][m['id']]
            if 'times' not in edge.keys():
                edge['times'] = []

            edge['times'].append(parser.parse(tweet_json['created_at'])) 

        
    """
    This function loads the tweets in a directory.
    """
    def _load_directory(self, G, dir):
        x = 0
        ids = os.listdir(dir)
        for tweet_id in ids:
            node_id = self._load_tweet(tweet_id, G, dir)
            rnode_ids = self._load_reactions(tweet_id, G, dir)
            self._load_tweet_annotations(tweet_id, G, dir, node_id)
            self._guilt_by_reaction(tweet_id, G, dir, rnode_ids)
            x += 1
            print(f'\rLoaded {x / len(ids) * 100:.1f}% tweets from {dir}', end="")
        print(f'\rLoaded 100.0% of tweets from {dir}')


    """
    This function classifies all nodes in the graph as rumour-spreaders and non-rumour-spreaders
    """
    def _classify(self, G):
        for n in G.nodes:
            rc = G.nodes[n].get('rumourCount', 0)
            nrc = G.nodes[n].get('nonRumourCount', 0)
            G.nodes[n]['isSpreadingRumours'] = (rc > nrc)



def stringizer(value):
    if type(value) == datetime.datetime:
        return str(value)
    raise TypeError


def destringizer(s):
    if s[:5] == "2015-":
        return parser.parse(s)
    else:
        raise ValueError


if __name__ == "__main__":
    main()
