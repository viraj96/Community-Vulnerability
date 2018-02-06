
from sklearn.metrics.cluster import adjusted_rand_score
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
parser.add_argument('--glo_metric', type = str, nargs = '+', help = 'Global metric to be used for greedy approach to select community.', choices = ['link_density', 'degree', 'conductance', 'compact'])
parser.add_argument('--com_metric', type = str, nargs = '+', help = 'Community centric metric to be used for greedy approach.', choices = ['clusteringCoeff', 'localMod', 'degreeCenter', 'betweenCenter', 'eigenCenter', 'closeCenter', 'coreness', 'diversity', 'eccentricity', 'constraint', 'closeVital', 'myMod', 'myNMI', 'intraDegree'])
parser.add_argument('--value', type = str, nargs = '+', help = 'Value functions to minimise.', choices = ['modularity', 'nmi'])
parser.add_argument('--algo', type = str, nargs = '+', help = 'Community detection algorithm to run.', choices = ['louvain', 'edge_betweenness', 'fast_greedy', 'infomap', 'label_propagation', 'leading_eigenvector', 'multilevel', 'walktrap'])
parser.add_argument('--graph', type = str, nargs = '+', help = 'Graph to load.', choices = ['karate', 'football'])

args = parser.parse_args()

def storeFileAndPlots(fileName, graph, tempGraph, graphPartition, partition, plotName, budget, selection = None):
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
		# exit()
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
		# print(old)
		# print("----")
		# print(new)
		# print("====")
		# return ig.compare_communities(new_graphPartition, partition, method = 'nmi', remove_none = False)
		# print ig.compare_communities(old, new, method = 'adjusted_rand', remove_none = False)
		print(adjusted_rand_score(old, new))
		# exit()
		return ig.compare_communities(old, new, method = 'adjusted_rand', remove_none = False)

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

def localModularity(graph, algo):
	graphPartition = returnPartition(graph, algo)
	# print(len(graph.es))
	exit()

def compactness(subgraph):
	temp = np.matrix(subgraph.shortest_paths_dijkstra(mode = 3))
	initial = temp[temp != np.inf].sum()
	return np.sum(initial)*1.0/temp.shape[0]

def conductance(graph, subgraph, community):
	denominator = sum(subgraph.degree())
	graph_degree = graph.degree()
	subgraph_degree = subgraph.degree()
	counter = 0
	for vertex in xrange(graph.vcount()):
		if( vertex in community ):
			subgraph_degree[counter] = graph_degree[vertex] - subgraph_degree[counter]
			counter += 1
	numerator = sum(subgraph_degree)
	return  numerator*1.0/denominator

def best_partition(graph, graphPartition):
	partition_scores = []
	# print("------")
	# print(graphPartition)
	for vertex_set in graphPartition:
		subgraph = graph.subgraph(vertex_set)
		if( args.glo_metric[0] == 'degree' ):
			partition_scores.append(sum(subgraph.degree())*1.0/2)
			best_partition = np.argsort(partition_scores)[-1]
		elif( args.glo_metric[0] == 'conductance' ):
			partition_scores.append(conductance(graph, subgraph, vertex_set))
			best_partition = np.argsort(partition_scores)[0]
		elif( args.glo_metric[0] == 'link_density' ):
			partition_scores.append(subgraph.ecount()*2.0/(subgraph.vcount()*(subgraph.vcount()-1)))
			best_partition = np.argsort(partition_scores)[-1]
		elif( args.glo_metric[0] == 'compact' ):
			partition_scores.append(compactness(subgraph))
			best_partition = np.argsort(partition_scores)[0]
	# print(best_partition)
	# print("======")
	result = graph.subgraph(graphPartition[best_partition])
	result.vs["name"] = graphPartition[best_partition]
	return result

def best_node(graph, budget = 1):
	if( args.com_metric[0] == 'clusteringCoeff' ):
		nodes = np.array(graph.transitivity_local_undirected(mode = 'zero'))
		bestNodes = nodes.argsort()[-budget:][0]
	elif( args.com_metric[0] == 'localMod' ):
		localModularity(graph, args.algo[0])
	elif( args.com_metric[0] == 'myMod' ):
		nodes = np.array(modularityNodes(graph, returnPartition(graph, args.algo[0]), args.algo[0]))
		bestNodes = nodes.argsort()[-budget:][0]
	elif( args.com_metric[0] == 'myNMI' ):
		nodes = np.array(nmiNodes(graph, returnPartition(graph, args.algo[0]), args.value[0], args.algo[0]))
		bestNodes = nodes.argsort()[:budget][0] # ulta here	
	elif( args.com_metric[0] == 'degreeCenter' ):
		nodes = np.array(graph.degree())
		bestNodes = nodes.argsort()[-budget:][0]
	elif( args.com_metric[0] == 'betweenCenter' ):
		nodes = np.array(graph.betweenness(directed = False))
		bestNodes = nodes.argsort()[-budget:][0]
	elif( args.com_metric[0] == 'eigenCenter' ):
		nodes = np.array(graph.eigenvector_centrality(directed = False))
		bestNodes = nodes.argsort()[-budget:][0]
	elif( args.com_metric[0] == 'closeCenter' ):
		nodes = np.array(graph.closeness())
		bestNodes = nodes.argsort()[-budget:][0]
	elif( args.com_metric[0] == 'coreness' ):
		nodes = np.array(graph.coreness())
		bestNodes = nodes.argsort()[-budget:][0]
	elif( args.com_metric[0] == 'diversity' ):
		nodes = np.array(graph.diversity())
		bestNodes = nodes.argsort()[-budget:][0]
	elif( args.com_metric[0] == 'eccentricity' ):
		nodes = np.array(graph.eccentricity())
		bestNodes = nodes.argsort()[-budget:][0]
	elif( args.com_metric[0] == 'constraint' ):
		nodes = np.array(graph.constraint())
		bestNodes = nodes.argsort()[-budget:][0]
	elif( args.com_metric[0] == 'closeVital' ):
		nodes = np.array(closenessVitality(graph))
		bestNodes = nodes.argsort()[-budget:][0]
	elif( args.com_metric[0] == 'intraDegree' ):
		nodes = np.array(intraDegree(graph, args.algo[0]))
		bestNodes = nodes.argsort()[-budget:][0]
	nodesOfGraph = graph.vs["name"]
	# print("|||||")
	# print(nodesOfGraph)
	bestNodes = nodesOfGraph[bestNodes]
	# print(bestNodes)
	# print("+++++")
	# for item in tempGraph.vs["name"]:
		# print(item)
		# if( item == bestNodes ):
			# print("What!")
			# print(item)
			# print("What?")
	return bestNodes

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

tempGraph = graph.copy()
partition = graphPartition

if( args.budget ):
	budget = args.budget
else:
	budget = 5

tryAll = []

print("\nCalculating value scores...\n")

bottleneckStart = datetime.datetime.now()
tempGraph.vs["name"] = np.arange(tempGraph.vcount())

counter = 0
bestNodes = []
while( counter < budget ):
	bestGraph = best_partition(tempGraph, partition)
	# print("Name =")
	# print(bestGraph.vs["name"])
	node = best_node(bestGraph)
	# print(node)
	bestNodes.append(node)
	tempGraph.delete_vertices(node)
	partition = returnPartition(tempGraph, args.algo[0])	
	counter += 1

# print()
selection = []
nodesList = np.arange(graph.vcount())
for item in nodesList:
	if( item not in tempGraph.vs["name"] ):
		selection.append(item)
# selection = bestNodes
valueScore = returnScore(graph, tempGraph, graphPartition, partition, args.value[0], selection)

bottleneckEnd = datetime.datetime.now()

print("\nBottle Neck Time = {0} seconds\n").format((bottleneckEnd - bottleneckStart))

print("\nCompiling results...\n")

if( args.graph[0] == 'football' ):
	storeFileAndPlots("Final/Data/" + args.graph[0] + "/" + args.value[0] + "/" + args.algo[0] + "/" + args.glo_metric[0] + "_" + args.com_metric[0] + "_community_attack.dat", graph, tempGraph, graphPartition, partition, "Final/Plots/" + args.graph[0] + "/" + args.value[0] + "/" + args.algo[0] +  "/football_graph_community_attack_" + args.glo_metric[0] + "_" + args.com_metric[0], str(budget), bestNodes)
elif( args.graph[0] == 'karate' ):
	storeFileAndPlots("Final/Data/" + args.graph[0] + "/" + args.value[0] + "/" + args.algo[0] + "/" + args.glo_metric[0] + "_" + args.com_metric[0] + "_community_attack.dat", graph, tempGraph, graphPartition, partition, "Final/Plots/" + args.graph[0] + "/" + args.value[0] + "/" + args.algo[0] +  "/karate_club_graph_community_attack_" + args.glo_metric[0] + "_" + args.com_metric[0], str(budget), selection)

totalTimeEnd = datetime.datetime.now()
print("\nTotal Execution Time = {0}\n").format((totalTimeEnd - totalTimeStart))