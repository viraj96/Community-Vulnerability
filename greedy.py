import json
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

parser = argparse.ArgumentParser(description = 'Generate greedy answer based to BTP for given budget in Karate Club Network')
parser.add_argument('--budget', type = int, nargs = '?', help = 'Budget k (Unit cost formulation)')
parser.add_argument('--metric', type = str, nargs = '+', help = 'Metric to be used for greedy approach. Choices are degree, clustering coefficient and local modularity', choices = ['clusteringCoeff', 'localMod', 'degreeCenter', 'betweenCenter', 'eigenCenter', 'closeCenter', 'coreness', 'diversity', 'eccentricity', 'constraint', 'closeVital', 'myMod', 'myNMI', 'intraDegree', 'degree_interDegree'])
parser.add_argument('--value', type = str, nargs = '+', help = 'Value functions to minimise.', choices = ['modularity', 'nmi'])
parser.add_argument('--algo', type = str, nargs = '+', help = 'Community detection algorithm to run.', choices = ['louvain', 'edge_betweenness', 'fast_greedy', 'infomap', 'label_propagation', 'leading_eigenvector', 'multilevel', 'walktrap'])
parser.add_argument('--graph', type = str, nargs = '+', help = 'Graph to load.', choices = ['karate', 'football'])

args = parser.parse_args()

def storeFileAndPlots(fileName, graph, tempGraph, graphPartition, partition, plotName, budget, write_to_file, selection = None):
	vertex_label = []
	for i in range(graph.vcount()):
		if( i not in bestNodes ):
			vertex_label.append(i)	
	ig.plot(partition, plotName + str(budget) + ".png", mark_groups = True, vertex_label = vertex_label)
	file = open(fileName, 'w')
	score = returnScore(graph, tempGraph, graphPartition, partition, args.value[0], selection)
	for i in bestNodes:
		file.write(str(i) + " ")
	file.write("\nScore = " + str(score) + "\n")
	file.write(json.dumps(write_to_file))
	file.close()	

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

def returnScore(graph, tempGraph, graphPartition, partition, value, selection = None):
	if( value == 'modularity' ):
		graphModularity = graph.modularity(graphPartition)
		return graphModularity - tempGraph.modularity(partition)
	elif( value == 'nmi' ):
		new_graph = graph.copy()
		new_graph.vs["membership"] = graphPartition.membership
		new_graph.delete_vertices(selection)
		new_graphPartition = ig.VertexClustering(new_graph, new_graph.vs["membership"])
		# return ig.compare_communities(new_graphPartition, partition, method = 'nmi', remove_none = False)
		old = [0] * tempGraph.vcount()
		new = [0] * tempGraph.vcount()
		for idx, community in enumerate(new_graphPartition):
			for node in community:
				if( node < tempGraph.vcount() ):
					old[node] = idx
		for idx, community in enumerate(partition):
			for node in community:
				new[node] = idx
		print(old)
		print("----")
		print(new)
		print("====")
		# return ig.compare_communities(new_graphPartition, partition, method = 'nmi', remove_none = False)
		print ig.compare_communities(old, new, method = 'ari', remove_none = False)
		return ig.compare_communities(old, new, method = 'ari', remove_none = False)

def closenessVitality(graph):
	temp = np.matrix(graph.shortest_paths_dijkstra(mode = 3))
	initial = temp[temp != np.inf].sum()
	closeness_vitality = []
	for i in range(graph.vcount()):
		tempGraph = graph.copy()
		tempGraph.delete_vertices(i)
		vertex_cont = np.matrix(tempGraph.shortest_paths_dijkstra(mode = 3))
		closeness_vitality.append(initial - vertex_cont[vertex_cont != np.inf].sum())
	return closeness_vitality

def modularityNodes(graph, graphPartition, algo):
	graphModularity = graph.modularity(graphPartition)
	best_mod = []
	for i in range(graph.vcount()):
		tempGraph = graph.copy()
		tempGraph.delete_vertices(i)
		partition = returnPartition(tempGraph, algo)
		modularity = tempGraph.modularity(partition)
		best_mod.append(graphModularity - modularity)
	return best_mod

def nmiNodes(graph, graphPartition, value, algo):
	best_nmi = []
	for i in range(graph.vcount()):
		tempGraph = graph.copy()
		tempGraph.delete_vertices(i)
		score = returnScore(graph, tempGraph, graphPartition, returnPartition(tempGraph, algo), value, selection = i)
		best_nmi.append(score)	
	return best_nmi

def intraDegree(graph, algo):
	intra_degree_values = np.zeros(len(graph.vs))
	graphPartition = returnPartition(graph, algo)
	for cluster in graphPartition:
		tuples = combinations(cluster, 2)
		for first, second in tuples:
			edges = graph.es.select(_within = [first, second])
			for e in edges:
				intra_degree_values[e.tuple[0]] += 1
				intra_degree_values[e.tuple[1]] += 1
	return intra_degree_values

def interDegree(graph, algo, graphPartition):
	inter_degree_values = np.zeros(len(graph.vs))
	edge_list = graph.get_edgelist()
	rejects = []
	for first, second in edge_list:
		for cluster in graphPartition:
			if( first in cluster and second in cluster ):
				rejects.append((first, second))
	for edge in edge_list:
		if( edge not in rejects ):
			inter_degree_values[edge[0]] += 1
			inter_degree_values[edge[1]] += 1
	return inter_degree_values

def localModularity(graph, algo):
	graphPartition = returnPartition(graph, algo)
	print(len(graph.es))
	exit()

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

f = open("Final/Data/" + args.graph[0] + "/" + args.value[0] + "/" + args.algo[0] + "_partition.pkl", "rb")
graphPartition = pickle.load(f)
f.close()

graph = graphPartition.graph

# interDegree(graph, args.algo[0], graphPartition)
# exit()

if( args.budget ):
	budget = args.budget
else:
	budget = 5

tryAll = []

print("\nCalculating value scores...\n")

bottleneckStart = datetime.datetime.now()

tempGraph = graph.copy()

if( args.metric[0] == 'clusteringCoeff' ):
	nodes = np.array(tempGraph.transitivity_local_undirected(mode = 'zero'))
	bestNodes = nodes.argsort()[-budget:][::-1]
elif( args.metric[0] == 'localMod' ):
	localModularity(tempGraph, args.algo[0])
elif( args.metric[0] == 'myMod' ):
	nodes = np.array(modularityNodes(tempGraph, returnPartition(tempGraph, args.algo[0]), args.algo[0]))
	bestNodes = nodes.argsort()[-budget:][::-1]
elif( args.metric[0] == 'myNMI' ):
	nodes = np.array(nmiNodes(tempGraph, returnPartition(tempGraph, args.algo[0]), args.value[0], args.algo[0]))
	bestNodes = nodes.argsort()[:budget][::-1] # ulta here	
elif( args.metric[0] == 'degreeCenter' ):
	nodes = np.array(tempGraph.degree())
	bestNodes = nodes.argsort()[-budget:][::-1]
elif( args.metric[0] == 'betweenCenter' ):
	nodes = np.array(tempGraph.betweenness(directed = False))
	bestNodes = nodes.argsort()[-budget:][::-1]
elif( args.metric[0] == 'eigenCenter' ):
	nodes = np.array(tempGraph.eigenvector_centrality(directed = False))
	bestNodes = nodes.argsort()[-budget:][::-1]
elif( args.metric[0] == 'closeCenter' ):
	nodes = np.array(tempGraph.closeness())
	bestNodes = nodes.argsort()[-budget:][::-1]
elif( args.metric[0] == 'coreness' ):
	nodes = np.array(tempGraph.coreness())
	bestNodes = nodes.argsort()[-budget:][::-1]
elif( args.metric[0] == 'diversity' ):
	nodes = np.array(tempGraph.diversity())
	bestNodes = nodes.argsort()[-budget:][::-1]
elif( args.metric[0] == 'eccentricity' ):
	nodes = np.array(tempGraph.eccentricity())
	bestNodes = nodes.argsort()[-budget:][::-1]
elif( args.metric[0] == 'constraint' ):
	nodes = np.array(tempGraph.constraint())
	bestNodes = nodes.argsort()[-budget:][::-1]
elif( args.metric[0] == 'closeVital' ):
	nodes = np.array(closenessVitality(tempGraph))
	bestNodes = nodes.argsort()[-budget:][::-1]
elif( args.metric[0] == 'intraDegree' ):
	nodes = np.array(intraDegree(tempGraph, args.algo[0]))
	bestNodes = nodes.argsort()[-budget:][::-1]
elif( args.metric[0] == 'degree_interDegree' ):
	degrees = np.array(tempGraph.degree())
	# print(degrees)
	array = np.arange(len(degrees))
	# print(array)
	nodes = np.array(interDegree(tempGraph, args.algo[0], graphPartition))
	# print(nodes)
	inter = zip(array, nodes)
	tuples = zip(degrees, inter)
	print(tuples)
	exit()
	tuples.sort(key = lambda x: x[0])
	print(tuples)
	exit()
	bestNodes = nodes.argsort()[-budget:][::-1]

write_to_file = dict()
for idx, node in enumerate(nodes):
	write_to_file[idx] = node

tryAll = bestNodes
tempGraph.delete_vertices(bestNodes)
valueScore = 0
selection = bestNodes

if( args.algo[0] == 'louvain' ):
	partition = louvain.find_partition(tempGraph, method = 'Modularity')
	valueScore = returnScore(graph, tempGraph, graphPartition, partition, args.value[0], selection)
elif( args.algo[0] == 'edge_betweenness' ):
	dendrogram = tempGraph.community_edge_betweenness(directed = False)
	fix_dendrogram(tempGraph, dendrogram)
	partition = dendrogram.as_clustering()
	valueScore = returnScore(graph, tempGraph, graphPartition, partition, args.value[0], selection)
elif( args.algo[0] == 'fast_greedy' ):
	dendrogram = tempGraph.community_fastgreedy()
	partition = dendrogram.as_clustering()
	valueScore = returnScore(graph, tempGraph, graphPartition, partition, args.value[0], selection)
elif( args.algo[0] == 'infomap' ):
	partition = tempGraph.community_infomap()
	valueScore = returnScore(graph, tempGraph, graphPartition, partition, args.value[0], selection)
elif( args.algo[0] == 'label_propagation' ):
	partition = tempGraph.community_label_propagation()
	valueScore = returnScore(graph, tempGraph, graphPartition, partition, args.value[0], selection)
elif( args.algo[0] == 'leading_eigenvector' ):
	partition = tempGraph.community_leading_eigenvector()
	valueScore = returnScore(graph, tempGraph, graphPartition, partition, args.value[0], selection)
elif( args.algo[0] == 'multilevel' ):
	partition = tempGraph.community_multilevel()
	valueScore = returnScore(graph, tempGraph, graphPartition, partition, args.value[0], selection)
elif( args.algo[0] == 'walktrap' ):
	dendrogram = tempGraph.community_walktrap()
	partition = dendrogram.as_clustering()
	valueScore = returnScore(graph, tempGraph, graphPartition, partition, args.value[0], selection)

bottleneckEnd = datetime.datetime.now()

print("\nBottle Neck Time = {0} seconds\n").format((bottleneckEnd - bottleneckStart))

print("\nCompiling results...\n")

if( args.graph[0] == 'football' ):
	storeFileAndPlots("Final/Data/" + args.graph[0] + "/" + args.value[0] + "/" + args.algo[0] + "/" + args.metric[0] + ".dat", graph, tempGraph, graphPartition, partition, "Final/Plots/" + args.graph[0] + "/" + args.value[0] + "/" + args.algo[0] +  "/football_graph_", args.metric[0] + "_" + str(budget), write_to_file, bestNodes)
elif( args.graph[0] == 'karate' ):
	storeFileAndPlots("Final/Data/" + args.graph[0] + "/" + args.value[0] + "/" + args.algo[0] + "/" + args.metric[0] + ".dat", graph, tempGraph, graphPartition, partition, "Final/Plots/" + args.graph[0] + "/" + args.value[0] + "/" + args.algo[0] +  "/karate_club_graph_", args.metric[0] + "_" + str(budget), write_to_file, bestNodes)

totalTimeEnd = datetime.datetime.now()
print("\nTotal Execution Time = {0}\n").format((totalTimeEnd - totalTimeStart))