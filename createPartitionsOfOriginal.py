import pickle
import louvain
import argparse
import datetime
import operator
import community
import numpy as np
import igraph as ig
import matplotlib.pyplot as plot
from itertools import permutations, combinations, izip

parser = argparse.ArgumentParser(description = 'Generate exhaustive answer to BTP for given budget in Complex Networks')
parser.add_argument('--budget', type = int, nargs = '?', help = 'Budget k (Unit cost formulation).')
parser.add_argument('--value', type = str, nargs = '+', help = 'Value functions to minimise.', choices = ['modularity', 'nmi', 'ari', 'purity'])
parser.add_argument('--algo', type = str, nargs = '+', help = 'Community detection algorithm to run.', choices = ['louvain', 'edge_betweenness', 'fast_greedy', 'infomap', 'label_propagation', 'leading_eigenvector', 'multilevel', 'walktrap'])
parser.add_argument('--graph', type = str, nargs = '+', help = 'Graph to load.', choices = ['karate', 'football', 'railway', 'citation'])

args = parser.parse_args()

def load_karate_club_graph():
	graph = ig.read('karate/karate.gml')
	graph.simplify()
	return graph

def load_football_graph():
	graph = ig.read('footballTSEweb/footballTSEinput.gml')
	graph.simplify()
	return graph

def fix_dendrogram(graph, cl):
    already_merged = set()
    for merge in cl.merges:
        already_merged.update(merge)

    num_dendrogram_nodes = graph.vcount() + len(cl.merges)
    not_merged_yet = sorted(set(xrange(num_dendrogram_nodes)) - already_merged)
    if len(not_merged_yet) < 2:
        return

    v1, v2 = not_merged_yet[:2]
    cl._merges.append((v1, v2))
    del not_merged_yet[:2]

    missing_nodes = xrange(num_dendrogram_nodes,
            num_dendrogram_nodes + len(not_merged_yet))
    cl._merges.extend(izip(not_merged_yet, missing_nodes))
    cl._nmerges = graph.vcount()-1

totalTimeStart = datetime.datetime.now()
print("\nStarting code...\n")

if( args.graph[0] == 'karate' ):
	graph = load_karate_club_graph()
elif( args.graph[0] == 'football' ):
	graph = load_football_graph()

graph.vs['name'] = np.arange(graph.vcount())

def returnPartition(graph, algo):
	if( algo == 'louvain' ):
		graphPartition = louvain.find_partition(graph, method = 'Modularity')
		return graphPartition
	elif( algo == 'edge_betweenness' ):
		dendrogram = graph.community_edge_betweenness(directed = False)
		graphPartition = dendrogram.as_clustering()
		return graphPartition
	elif( algo == 'fast_greedy' ):
		dendrogram = graph.community_fastgreedy()
		graphPartition = dendrogram.as_clustering()
		return graphPartition
	elif( algo == 'infomap' ):
		graphPartition = graph.community_infomap()
		return graphPartition
	elif( algo == 'label_propagation' ):
		graphPartition = graph.community_label_propagation()
		return graphPartition
	elif( algo == 'leading_eigenvector' ):
		graphPartition = graph.community_leading_eigenvector()
		return graphPartition
	elif( algo == 'multilevel' ):
		graphPartition = graph.community_multilevel()
		return graphPartition
	elif( algo == 'walktrap' ):
		dendrogram = graph.community_walktrap()
		graphPartition = dendrogram.as_clustering()
		return graphPartition

graphPartition = returnPartition(graph, args.algo[0])
with open("Final/Data/" + args.graph[0] + "/" + args.value[0] + "/" + args.algo[0] + "/partition.pkl", "wb") as handle:
	pickle.dump(graphPartition, handle)
with open("Final/Data/" + args.graph[0] + "/" + args.value[0] + "/" + args.algo[0] + "/graph.pkl", "wb") as handle:
	pickle.dump(graph, handle)

if( args.graph[0] == 'karate' ):
	plt = ig.plot(graphPartition, "Final/Plots/" + args.graph[0] + "/original/" + args.algo[0] + ".png", mark_groups = True, vertex_label = [i for i in range(graph.vcount())])
elif( args.graph[0] == 'football' ):
	plt = ig.plot(graphPartition, "Final/Plots/" + args.graph[0] + "/original/" + args.algo[0] + ".png", mark_groups = True, vertex_label = [i for i in range(graph.vcount())])