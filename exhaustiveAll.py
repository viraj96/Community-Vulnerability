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

parser = argparse.ArgumentParser(description = 'Generate exhaustive all answer to BTP for given budget in Complex Networks')
parser.add_argument('--budget', type = int, nargs = '?', help = 'Budget k (Unit cost formulation).')
parser.add_argument('--value', type = str, nargs = '+', help = 'Value functions to minimise.', choices = ['modularity', 'nmi', 'ari', 'purity'])
parser.add_argument('--algo', type = str, nargs = '+', help = 'Community detection algorithm to run.', choices = ['louvain', 'edge_betweenness', 'fast_greedy', 'infomap', 'label_propagation', 'leading_eigenvector', 'multilevel', 'walktrap'])
parser.add_argument('--graph', type = str, nargs = '+', help = 'Graph to load.', choices = ['karate', 'football', 'railway', 'citation'])

args = parser.parse_args()

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

f = open("Final/Data/" + args.graph[0] + "/" + args.value[0] + "/" + args.algo[0] + "/graph.pkl", "rb")
graph = pickle.load(f)
f.close()

f = open("Final/Data/" + args.graph[0] + "/" + args.value[0] + "/" + args.algo[0] + "/partition.pkl", "rb")
graphPartition = pickle.load(f)
f.close()

if( args.budget ):
	budget = args.budget
else:
	budget = 5

totalNodes = graph.vcount()
nodesList = np.arange(totalNodes)
tryAll = []

print("\nStarting combinations code...\n")

combinationsStart = datetime.datetime.now()
for val in combinations(nodesList, budget):
	allPerms = list(permutations(val))
	for perm in allPerms:
		tryAll.append(perm)
tryAll = np.array(tryAll)
print("Length of combinations = {0}\n").format(len(tryAll))
combinationsEnd = datetime.datetime.now()

print("\nCombinations Time = {0} seconds\n").format(combinationsEnd - combinationsStart)

valueScores = []

print("\nCalculating value scores...\n")

def returnScore(graph, graphPartition, partition, value, selection = None):
	if( value == 'modularity' ):
		graphModularity = graphPartition.modularity
		return ((graphModularity - partition.modularity)/graphModularity)*100
	elif( value == 'nmi' ):
		new_graph = graph.copy()
		new_graph.vs["membership"] = graphPartition.membership
		new_graph.delete_vertices(selection)
		new_graphPartition = ig.VertexClustering(new_graph, new_graph.vs["membership"])
		old = [0] * tempGraph.vcount()
		new = [0] * tempGraph.vcount()
		for idx, community in enumerate(new_graphPartition):
			for node in community:
				if( node < tempGraph.vcount() ):
					old[node] = idx
		for idx, community in enumerate(partition):
			for node in community:
				new[node] = idx
		# return ig.compare_communities(new_graphPartition, partition, method = 'nmi', remove_none = False)
		# print ig.compare_communities(old, new, method = 'ari', remove_none = False)
		return ig.compare_communities(old, new, method = 'ari', remove_none = False)

maxVal = -1000
bestGraphPartition = None

bottleneckStart = datetime.datetime.now()
for idx, selection in enumerate(tryAll):
	if( idx % 10000 == 0 and idx != 0 ):
		print("{0} combinations done!!").format(idx + 1)
	tempGraph = graph.copy()
	tempGraph.delete_vertices(selection)
	if( args.algo[0] == 'louvain' ):
		partition = louvain.find_partition(tempGraph, method = 'Modularity')
	elif( args.algo[0] == 'edge_betweenness' ):
		dendrogram = tempGraph.community_edge_betweenness(directed = False)
		fix_dendrogram(tempGraph, dendrogram)
		partition = dendrogram.as_clustering()
	elif( args.algo[0] == 'fast_greedy' ):
		dendrogram = tempGraph.community_fastgreedy()
		partition = dendrogram.as_clustering()		
	elif( args.algo[0] == 'infomap' ):
		partition = tempGraph.community_infomap()
	elif( args.algo[0] == 'label_propagation' ):
		partition = tempGraph.community_label_propagation()
	elif( args.algo[0] == 'leading_eigenvector' ):
		partition = tempGraph.community_leading_eigenvector()
	elif( args.algo[0] == 'multilevel' ):
		partition = tempGraph.community_multilevel()		
	elif( args.algo[0] == 'walktrap' ):
		dendrogram = tempGraph.community_walktrap()
		partition = dendrogram.as_clustering()
	score = returnScore(graph, graphPartition, partition, args.value[0], selection)
	if( maxVal <= score ):
		maxVal = score
		bestGraphPartition = partition
	valueScores.append(score)

bottleneckEnd = datetime.datetime.now()

print("\nBottle Neck Time = {0} seconds\n").format(bottleneckEnd - bottleneckStart)

print("\nCompiling results...\n")

tupledTryAll = []
for element in tryAll:
	tupledTryAll.append(tuple(element))

valueScores = np.array(valueScores)
scores = dict(zip(tupledTryAll, valueScores))
if( args.value[0] == 'modularity' ):
	scoresSorted = sorted(scores.items(), key = operator.itemgetter(1), reverse = True)
elif( args.value[0] == 'nmi' ):
	scoresSorted = sorted(scores.items(), key = operator.itemgetter(1), reverse = False)
bestNodes = np.array(scoresSorted[0][0])

vertex_label = []
for i in range(graph.vcount()):
	if( i not in bestNodes ):
		vertex_label.append(i)

if( args.graph[0] == 'karate' ):
	plt = ig.plot(bestGraphPartition, "Final/Plots/" + args.graph[0] + "/" + args.value[0] + "/" + args.algo[0] + "/exhaustive_all_" + str(budget) + ".png", mark_groups = True, vertex_label = vertex_label)
elif( args.graph[0] == 'football' ):
	plt = ig.plot(bestGraphPartition, "Final/Plots/" + args.graph[0] + "/" + args.value[0] + "/" + args.algo[0] + "/exhaustive_all_" + str(budget) + ".png", mark_groups = True, vertex_label = vertex_label)

exhaustiveFile = open("Final/Data/" + args.graph[0] + "/" + args.value[0] + "/" + args.algo[0] + "/exhaustive_results_all_" + str(budget) + ".dat", 'w')
exhaustiveFile.write("<------------------Final Exhaustive Scores------------------>\n")
for result in scoresSorted:
	exhaustiveFile.write("%s\n" % str(result))
exhaustiveFile.close()

totalTimeEnd = datetime.datetime.now()
print("\nTotal Execution Time = {0}\n").format(totalTimeEnd - totalTimeStart)