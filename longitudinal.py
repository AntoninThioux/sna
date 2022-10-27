"""
This file contains the logic for the longitudinal analysis of the network.
"""

import networkx as nx
from plots import *

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
