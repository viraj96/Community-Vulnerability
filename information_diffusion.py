import louvain
import linkpred
import numpy as np
import igraph as ig
import networkx as nx
from bokeh.io import show
import ndlib.models.ModelConfig	as mc
from ndlib.viz.bokeh.MultiPlot import MultiPlot
import ndlib.models.epidemics.ThresholdModel as tm
from ndlib.viz.bokeh.DiffusionTrend import DiffusionTrend
from ndlib.viz.bokeh.DiffusionPrevalence import DiffusionPrevalence

vm = MultiPlot()

# load graph
print("Loading the graph!")
ig_graph = ig.Graph.Read_Ncol("coauthorship_network", directed = False)
edge_list = ig_graph.get_edgelist()
print(len(edge_list))
nx_graph = nx.Graph(edge_list)

# model instantiation
print("Model instantiation!")
model = tm.ThresholdModel(nx_graph)

# config parameters
print("Setting the parameters of the model!")
config = mc.Configuration()
config.add_model_parameter("percentage_infected", 0.30)
for n in nx_graph.nodes():
	config.add_node_configuration("threshold", n, 0.40)
model.set_initial_status(config)

# execute simulation
print("Running simulations!")
iterations = model.iteration_bunch(10, node_status = True)
trends = model.build_trends(iterations)

# visualizations
print("Plotting the visualization!")
viz = DiffusionTrend(model, trends)
plot = viz.plot(width = 400, height = 400)
vm.add_plot(plot)

# community based approach
def best_partition(graph, graphPartition):
	partition_scores = []
	for vertex_set in graphPartition:
		subgraph = graph.subgraph(vertex_set)
		partition_scores.append(sum(subgraph.degree()))
		best_partition = np.argsort(partition_scores)[-1]
	result = graph.subgraph(graphPartition[best_partition])
	result.vs["name"] = graphPartition[best_partition]
	return result

print("Community based approach started!")
budget = 4
counter = 0
temp_graph = ig_graph.copy()
partition = louvain.find_partition(ig_graph, method = "Modularity")

while(counter < budget):
	subgraph = best_partition(temp_graph, partition)
	temp_graph.delete_vertices(np.array(subgraph.degree()).argsort()[-1:][0])
	partition = louvain.find_partition(temp_graph, method = "Modularity")
	counter += 1

edge_list_new = temp_graph.get_edgelist()
print(len(edge_list_new))
nx_graph_new = nx.Graph(edge_list_new)

print("Running new simulations!")
model_new = tm.ThresholdModel(nx_graph_new)
config_new = mc.Configuration()
config_new.add_model_parameter("percentage_infected", 0.30)
for n in nx_graph_new.nodes():
	config_new.add_node_configuration("threshold", n, 0.40)
model_new.set_initial_status(config_new)
iterations_new = model_new.iteration_bunch(10)
trends_new = model_new.build_trends(iterations_new)
viz_new = DiffusionTrend(model_new, trends_new)
plot_new = viz_new.plot(width = 400, height = 400)
vm.add_plot(plot_new)

show(vm.plot())