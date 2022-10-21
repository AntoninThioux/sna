"""
This file contains the logic for loading the raw data in networkx graphs
"""

import networkx as nx
import json
import os

PATH = "./charliehebdo-all-rnr-threads/"


def main():
    print('Trying to load graph...')
    G = load_rnr_graph(PATH)
    print('Rumours/non-rumour graph loaded successfully!')


"""
This function loads a single annotated tweet in the dataset.
"""
def load_tweet(tid, G, path):
    f = open(path + f'{tid}/source-tweets/{tid}.json')
    tweet = json.load(f)
    f.close()
    G.add_edges_from([(tweet['user']['id'], mention['id']) for mention in tweet['entities']['user_mentions']])


"""
This function loads the reactions to a tweet in the dataset.
"""
def load_reactions(tid, G, path):
    files = os.listdir(path + f'{tid}/reactions')
    for reaction_file in files:
        rf = open(path + f'{tid}/reactions/' + reaction_file)
        subtweet = json.load(rf)
        G.add_edges_from([(subtweet['user']['id'], mention['id']) for mention in subtweet['entities']['user_mentions']])
            
        rf.close()


"""
This function loads the tweets in a directory.
"""
def load_directory(G, dir):
    x = 0

    ids = os.listdir(dir)
    for tweet_id in ids:
        load_tweet(tweet_id, G, dir)
        load_reactions(tweet_id, G, dir)
        x += 1
        print(f'\rLoaded {x / len(ids) * 100:.1f}% tweets from {dir}',end="")
    
    print(f'\rLoaded 100.0% of tweets from {dir}')
    

"""
This function loads the graph.
"""
def load_rnr_graph(path):
    G = nx.Graph()
    load_directory(G, path + "rumours/")
    load_directory(G, path + "non-rumours/")
    return G


if __name__ == "__main__":
    main()