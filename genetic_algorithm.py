import random
import pickle
import louvain
import argparse
import datetime
import operator
import numpy as np
import igraph as ig
import matplotlib.pyplot as plot
from itertools import permutations

totalTimeStart = datetime.datetime.now()
print("\nStarting code...\n")

parser = argparse.ArgumentParser(description = 'Generate greedy answer based to BTP for given budget in Karate Club Network')
parser.add_argument('--budget', type = int, nargs = '?', help = 'Budget k (Unit cost formulation)')
parser.add_argument('--metric', type = str, nargs = '+', help = 'Metric to be used for greedy approach. Choices are degree, clustering coefficient and local modularity', choices = ['clusteringCoeff', 'localMod', 'degreeCenter', 'betweenCenter', 'eigenCenter', 'closeCenter', 'coreness', 'diversity', 'eccentricity', 'constraint', 'closeVital', 'myMod', 'myNMI', 'intraDegree'])
parser.add_argument('--value', type = str, nargs = '+', help = 'Value functions to minimise.', choices = ['modularity', 'nmi'])
parser.add_argument('--algo', type = str, nargs = '+', help = 'Community detection algorithm to run.', choices = ['louvain', 'edge_betweenness', 'fast_greedy', 'infomap', 'label_propagation', 'leading_eigenvector', 'multilevel', 'walktrap'])
parser.add_argument('--graph', type = str, nargs = '+', help = 'Graph to load.', choices = ['karate', 'football'])

args = parser.parse_args()

INIT_POP_SIZE = 100
BEST_FROM_GEN = 20
GENERATIONS = 200
SPLIT = 0.75

# f = open("Final/Data/" + args.graph[0] + "/" + args.value[0] + "/" + args.algo[0] + "_partition.pkl", "rb")
# graphPartition = pickle.load(f)
# f.close()

# graph = graphPartition.graph

def load_karate_club_graph():
	graph = ig.read('karate/karate.gml')
	graph.simplify()
	return graph

def load_football_graph():
	graph = ig.read('footballTSEweb/footballTSEinput.gml')
	graph.simplify()
	return graph

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

graph = load_football_graph()
graphPartition = returnPartition(graph, args.algo[0])

if( args.budget ):
	budget = args.budget
else:
	budget = 5

totalNodes = graph.vcount()
nodesList = np.arange(totalNodes)

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
		return ig.compare_communities(new_graphPartition, partition, method = 'nmi', remove_none = False)

def get_propagation(chromosomes):
	mating = []
	while( len(mating) != int((INIT_POP_SIZE - len(chromosomes))*SPLIT) ):
		parent1 = random.randint(0, len(chromosomes)-1)
		parent2 = random.randint(0, len(chromosomes)-1)
		if( parent1 != parent2 ):
			mating.append(chromosomes[parent1][:2] + chromosomes[parent2][2:])
	return mating

def get_mutation(chromosomes):
	mutate = []
	while( len(mutate) != int((INIT_POP_SIZE - len(chromosomes))*SPLIT/3) ):
		candidate = random.randint(0, len(chromosomes)-1)
		position = random.randint(0, budget-1)
		new = random.randint(0, totalNodes-1)
		temp = list(chromosomes[candidate])
		temp[position] = new
		mutate.append(tuple(temp))
	return mutate

def get_next_gen(chromosomes):
	propagation = get_propagation(chromosomes)
	mutation = get_mutation(chromosomes)
	return chromosomes + propagation + mutation

chromosomes = random.sample(list(permutations(nodesList, budget)), INIT_POP_SIZE)

generation = 1

maxVal = -1000
bestGraphPartition = None

while( generation != GENERATIONS ):
	print("Starting generation " + str(generation))
	random.shuffle(chromosomes)
	valueScores = []
	for selection in chromosomes:
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
		score = returnScore(graph, tempGraph, graphPartition, partition, args.value[0], selection)
		if( maxVal <= score ):
			maxVal = score
			bestGraphPartition = partition
		valueScores.append(score)
	valueScores = np.array(valueScores)
	scores = dict(zip(chromosomes, valueScores))
	scoresSorted = sorted(scores.items(), key = operator.itemgetter(1), reverse = True)
	chromosomes = [tupleVal[0] for  tupleVal in scoresSorted]
	chromosomes = chromosomes[:BEST_FROM_GEN]
	chromosomes = get_next_gen(chromosomes)
	generation += 1

bestNodes = np.array(scoresSorted[0][0])

vertex_label = []
for i in range(graph.vcount()):
	if( i not in bestNodes ):
		vertex_label.append(i)

if( args.graph[0] == 'karate' ):
	plt = ig.plot(bestGraphPartition, "Final/Plots/" + args.graph[0] + "/" + args.value[0] + "/" + args.algo[0] + "/karate_club_graph_genetic_" + str(budget) + ".png", mark_groups = True, vertex_label = vertex_label)
elif( args.graph[0] == 'football' ):
	plt = ig.plot(bestGraphPartition, "Final/Plots/" + args.graph[0] + "/" + args.value[0] + "/" + args.algo[0] + "/football_graph_genetic_" + str(budget) + ".png", mark_groups = True, vertex_label = vertex_label)

geneticFile = open("Final/Data/" + args.graph[0] + "/" + args.value[0] + "/" + args.algo[0] + "/geneticResults_" + str(budget) + ".dat", 'w')
geneticFile.write("<------------------Final Genetic Algorithm Scores------------------>\n")
for result in scoresSorted:
	geneticFile.write("%s\n" % str(result))
geneticFile.close()

totalTimeEnd = datetime.datetime.now()
print("\nTotal Execution Time = {0}\n").format(totalTimeEnd - totalTimeStart)