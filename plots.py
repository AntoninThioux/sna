"""
This file is resposible for creating and displaying the plots
"""

import matplotlib.pyplot as plt
import numpy as np

def degree_distribution(degrees):
    bins = np.array([25*x for x in range(20)])
    _, _, patches = plt.hist(degrees, bins=bins, edgecolor='white')
    for i in range(len(patches)):
        patches[i].set_facecolor(i % 2 * 'r' + (i + 1) % 2 * 'b')
    plt.yscale('log')
    plt.title('Node Degree Distribution')
    plt.xlabel('Degrees')
    plt.ylabel('Quantity of Nodes')
    plt.xticks(bins + 12.5, labels=[f"{x} - {x+25}" for x in bins], rotation=25)
    plt.xlim(left=-7.5,right=507.5)
    plt.show()


def centrality_distribution(centralities):
    bins = np.array([0.00125 * x for x in range(9)])
    _, _, patches = plt.hist(list(centralities.values()), bins=bins, edgecolor='white')
    for i in range(len(patches)):
        patches[i].set_facecolor(i % 2 * 'green' + (i + 1) % 2 * 'orange')
    plt.yscale('log')
    plt.title('Node Degree Centrality Distribution')
    plt.xlabel('Degree Centrality')
    plt.ylabel('Quantity of Nodes')
    plt.xticks(bins + 0.000625, labels=[f"{x:.5f} - {x+0.00125:.5f}" for x in bins], rotation=25)
    plt.xlim(left=-0.000625/2,right=0.01+0.000625/2)
    plt.show()


def clustering_distribution(clustering):
    bins = np.array([0.1 * x for x in range(11)])
    _, _, patches = plt.hist(list(clustering.values()), bins=bins, edgecolor='white')
    for i in range(len(patches)):
        patches[i].set_facecolor(i % 2 * 'dimgray' + (i + 1) % 2 * 'lightgray')
    plt.yscale('log')
    plt.title('Node Clustering Coeffient Distribution')
    plt.xlabel('Clustering Coeffient')
    plt.ylabel('Quantity of Nodes')
    plt.xticks(bins + 0.05, labels=[f"{x:.1f} - {x+0.1:.1f}" for x in bins], rotation=25)
    plt.xlim(left=-0.025,right=1.025)
    plt.show()
