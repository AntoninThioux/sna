"""
This file contains the logic for the longitudinal analysis of the network.
"""

import networkx as nx

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

    