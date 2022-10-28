"""
This file contains the logic for the longitudinal analysis of the network.
"""

import networkx as nx
import os
import json
from dateutil import parser
import numpy as np

from plots import *
from convert_veracity_annotations import convert_annotations


PATH = "./charliehebdo-all-rnr-threads/"


"""
This function returns the activity of a node
"""
def node_activity(D, n, out=False):
    activity = []
    edge_times = None

    if out:
        edge_times = D.out_edges(n, 'times')
    else:
        edge_times = D.in_edges(n, 'times')

    for _, _, times in edge_times:
        activity += times

    first = min(activity)
    return sorted([int((t - first).total_seconds()) for t in activity])


"""
This is a cool lil algorithm to get the running count of responses within a window (size x) in O(n) time.
"""
def responses_per_X(activity, x=60):
    n = activity[-1] + x
    per_X = [0] * n
    l, r = 0, 0
    for i in range(n):
        while i - x >= activity[l]:
            l += 1
        while r < len(activity) and i >= activity[r]:
            r += 1
        per_X[i] = (r - 1) - (l - 1)
    return per_X


"""
This function plots the activity of the network
"""
def network_activity(D, hubs=None, authorities=None):
    if not hubs or not authorities:
        hubs, authorities = nx.hits(D)

    max_hub = max(hubs, key=hubs.get)
    max_hub_activity = node_activity(D, max_hub, out=True)
    hub_rpm = responses_per_X(max_hub_activity, 60)
    hub_rph = responses_per_X(max_hub_activity, 60*60)
    plot_activity(hub_rpm, hub_rph, title="Max hub out activity")

    max_authority = max(authorities, key=authorities.get)
    max_authority_activity = node_activity(D, max_authority)
    authority_rpm = responses_per_X(max_authority_activity, 60)
    authority_rph = responses_per_X(max_authority_activity, 60*60)
    plot_activity(authority_rpm, authority_rph, title="Max authority in activity")


"""
This function plots the evolution of rumour and non-rumours in the network.
"""
def network_evolution():
    rumours, nonrumours = rnr_frequenies()
    rumours_share, nonrumours_share = running_share(rumours, nonrumours)
    plot_share(rumours_share, nonrumours_share, 'Share of rumours and Non-Rumours', ['rumour share', 'non-rumour share'])

    facts, nonfacts = missinformation_frequencies()
    nonfact_share, fact_share = running_share(nonfacts, facts)
    plot_share(nonfact_share, fact_share, 'Share of missinformation in rumours', ['missinformation share', 'fact share'])


"""
This function returns the rumour nonrumour frequencies
"""
def rnr_frequenies(path=PATH):
    r_times = []
    r_ids = os.listdir(path + 'rumours')
    for tweet_id in r_ids:
        with open(path + f'rumours/{tweet_id}/source-tweets/{tweet_id}.json') as f:
            tweet = json.load(f)
            r_times.append(parser.parse(tweet['created_at']))
    
    nr_times = []
    nr_ids = os.listdir(path + 'non-rumours')
    for tweet_id in nr_ids:
        with open(path + f'non-rumours/{tweet_id}/source-tweets/{tweet_id}.json') as f:
            tweet = json.load(f)
            nr_times.append(parser.parse(tweet['created_at']))

    sorted_r_times, sorted_nr_times  = np.array(sorted(r_times)), np.array(sorted(nr_times))
    start = min(sorted_r_times[0], sorted_nr_times[0])
    to_seconds = np.vectorize(lambda x : int((x - start).total_seconds()))
    return to_seconds(sorted_r_times), to_seconds(sorted_nr_times)


"""
Computes the running share of two arrays in O(n).
"""
def running_share(a, b):
    c = np.array([0.0] * (max(a[-1], b[-1]) + 1))
    d = np.array([1.0] * (max(a[-1], b[-1]) + 1))

    ai, bi = 0, 0
    total_a, total_b = 0, 0
    for i in range(len(c)):
        while ai < len(a) and a[ai] <= i:
            total_a += 1
            ai += 1
        while bi < len(b) and b[bi] <= i:
            total_b += 1
            bi += 1
        c[i] = float(total_a) / float(total_a + total_b)

    return c, d - c


"""
This function plots the missinformation frequencies
"""
def missinformation_frequencies(path=PATH):
    f_times = []
    nf_times = []

    ids = os.listdir(path + 'rumours')
    for t_id in ids:
        with open(path + f'rumours/{t_id}/source-tweets/{t_id}.json') as t, open(path + f'rumours/{t_id}/annotation.json') as a:
            tweet = json.load(t)
            anno = json.load(a)
            if convert_annotations(anno) == 'true':
                f_times.append(parser.parse(tweet['created_at']))
            elif convert_annotations(anno) == 'false':
                nf_times.append(parser.parse(tweet['created_at']))

    sorted_f_times, sorted_nf_times  = np.array(sorted(f_times)), np.array(sorted(nf_times))
    start = min(sorted_f_times[0], sorted_nf_times[0])
    to_seconds = np.vectorize(lambda x : int((x - start).total_seconds()))
    return to_seconds(sorted_f_times), to_seconds(sorted_nf_times)


if __name__ == "__main__":
    network_evolution()
