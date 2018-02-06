#!/bin/bash

echo "Starting modularity value.."

echo "Starting louvain.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value modularity --algo louvain --graph karate
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value modularity --algo louvain --graph karate
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value modularity --algo louvain --graph karate
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value modularity --algo louvain --graph karate
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value modularity --algo louvain --graph karate
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value modularity --algo louvain --graph karate
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value modularity --algo louvain --graph karate
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value modularity --algo louvain --graph karate
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value modularity --algo louvain --graph karate
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value modularity --algo louvain --graph karate
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value modularity --algo louvain --graph karate
echo "Starting intra degree.."
python greedy.py --budget 4 --metric intraDegree --value modularity --algo louvain --graph karate

echo "Starting edge_betweenness.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value modularity --algo edge_betweenness --graph karate
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value modularity --algo edge_betweenness --graph karate
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value modularity --algo edge_betweenness --graph karate
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value modularity --algo edge_betweenness --graph karate
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value modularity --algo edge_betweenness --graph karate
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value modularity --algo edge_betweenness --graph karate
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value modularity --algo edge_betweenness --graph karate
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value modularity --algo edge_betweenness --graph karate
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value modularity --algo edge_betweenness --graph karate
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value modularity --algo edge_betweenness --graph karate
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value modularity --algo edge_betweenness --graph karate
echo "Starting intra degree.."
python greedy.py --budget 4 --metric intraDegree --value modularity --algo edge_betweenness --graph karate

echo "Starting fast_greedy.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value modularity --algo fast_greedy --graph karate
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value modularity --algo fast_greedy --graph karate
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value modularity --algo fast_greedy --graph karate
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value modularity --algo fast_greedy --graph karate
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value modularity --algo fast_greedy --graph karate
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value modularity --algo fast_greedy --graph karate
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value modularity --algo fast_greedy --graph karate
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value modularity --algo fast_greedy --graph karate
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value modularity --algo fast_greedy --graph karate
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value modularity --algo fast_greedy --graph karate
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value modularity --algo fast_greedy --graph karate
echo "Starting intra degree.."
python greedy.py --budget 4 --metric intraDegree --value modularity --algo fast_greedy --graph karate

echo "Starting infomap.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value modularity --algo infomap --graph karate
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value modularity --algo infomap --graph karate
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value modularity --algo infomap --graph karate
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value modularity --algo infomap --graph karate
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value modularity --algo infomap --graph karate
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value modularity --algo infomap --graph karate
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value modularity --algo infomap --graph karate
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value modularity --algo infomap --graph karate
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value modularity --algo infomap --graph karate
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value modularity --algo infomap --graph karate
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value modularity --algo infomap --graph karate
echo "Starting intra degree.."
python greedy.py --budget 4 --metric intraDegree --value modularity --algo infomap --graph karate

echo "Starting label_propagation.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value modularity --algo label_propagation --graph karate
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value modularity --algo label_propagation --graph karate
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value modularity --algo label_propagation --graph karate
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value modularity --algo label_propagation --graph karate
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value modularity --algo label_propagation --graph karate
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value modularity --algo label_propagation --graph karate
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value modularity --algo label_propagation --graph karate
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value modularity --algo label_propagation --graph karate
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value modularity --algo label_propagation --graph karate
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value modularity --algo label_propagation --graph karate
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value modularity --algo label_propagation --graph karate
echo "Starting intra degree.."
python greedy.py --budget 4 --metric intraDegree --value modularity --algo label_propagation --graph karate

echo "Starting leading_eigenvector.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value modularity --algo leading_eigenvector --graph karate
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value modularity --algo leading_eigenvector --graph karate
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value modularity --algo leading_eigenvector --graph karate
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value modularity --algo leading_eigenvector --graph karate
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value modularity --algo leading_eigenvector --graph karate
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value modularity --algo leading_eigenvector --graph karate
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value modularity --algo leading_eigenvector --graph karate
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value modularity --algo leading_eigenvector --graph karate
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value modularity --algo leading_eigenvector --graph karate
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value modularity --algo leading_eigenvector --graph karate
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value modularity --algo leading_eigenvector --graph karate
echo "Starting intra degree.."
python greedy.py --budget 4 --metric intraDegree --value modularity --algo leading_eigenvector --graph karate

echo "Starting multilevel.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value modularity --algo multilevel --graph karate
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value modularity --algo multilevel --graph karate
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value modularity --algo multilevel --graph karate
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value modularity --algo multilevel --graph karate
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value modularity --algo multilevel --graph karate
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value modularity --algo multilevel --graph karate
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value modularity --algo multilevel --graph karate
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value modularity --algo multilevel --graph karate
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value modularity --algo multilevel --graph karate
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value modularity --algo multilevel --graph karate
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value modularity --algo multilevel --graph karate
echo "Starting intra degree.."
python greedy.py --budget 4 --metric intraDegree --value modularity --algo multilevel --graph karate

# echo "Starting spinglass.."
# python greedy.py --budget 4 --value modularity --algo spinglass

echo "Starting walktrap.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value modularity --algo walktrap --graph karate
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value modularity --algo walktrap --graph karate
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value modularity --algo walktrap --graph karate
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value modularity --algo walktrap --graph karate
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value modularity --algo walktrap --graph karate
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value modularity --algo walktrap --graph karate
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value modularity --algo walktrap --graph karate
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value modularity --algo walktrap --graph karate
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value modularity --algo walktrap --graph karate
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value modularity --algo walktrap --graph karate
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value modularity --algo walktrap --graph karate
echo "Starting intra degree.."
python greedy.py --budget 4 --metric intraDegree --value modularity --algo walktrap --graph karate

echo "Starting nmi value.."

echo "Starting louvain.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value nmi --algo louvain --graph karate
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value nmi --algo louvain --graph karate
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value nmi --algo louvain --graph karate
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value nmi --algo louvain --graph karate
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value nmi --algo louvain --graph karate
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value nmi --algo louvain --graph karate
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value nmi --algo louvain --graph karate
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value nmi --algo louvain --graph karate
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value nmi --algo louvain --graph karate
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value nmi --algo louvain --graph karate
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value nmi --algo louvain --graph karate
echo "Starting intra degree.."
python greedy.py --budget 4 --metric intraDegree --value nmi --algo louvain --graph karate

echo "Starting edge_betweenness.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value nmi --algo edge_betweenness --graph karate
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value nmi --algo edge_betweenness --graph karate
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value nmi --algo edge_betweenness --graph karate
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value nmi --algo edge_betweenness --graph karate
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value nmi --algo edge_betweenness --graph karate
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value nmi --algo edge_betweenness --graph karate
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value nmi --algo edge_betweenness --graph karate
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value nmi --algo edge_betweenness --graph karate
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value nmi --algo edge_betweenness --graph karate
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value nmi --algo edge_betweenness --graph karate
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value nmi --algo edge_betweenness --graph karate
echo "Starting intra degree.."
python greedy.py --budget 4 --metric intraDegree --value nmi --algo edge_betweenness --graph karate

echo "Starting fast_greedy.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value nmi --algo fast_greedy --graph karate
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value nmi --algo fast_greedy --graph karate
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value nmi --algo fast_greedy --graph karate
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value nmi --algo fast_greedy --graph karate
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value nmi --algo fast_greedy --graph karate
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value nmi --algo fast_greedy --graph karate
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value nmi --algo fast_greedy --graph karate
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value nmi --algo fast_greedy --graph karate
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value nmi --algo fast_greedy --graph karate
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value nmi --algo fast_greedy --graph karate
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value nmi --algo fast_greedy --graph karate
echo "Starting intra degree.."
python greedy.py --budget 4 --metric intraDegree --value nmi --algo fast_greedy --graph karate

echo "Starting infomap.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value nmi --algo infomap --graph karate
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value nmi --algo infomap --graph karate
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value nmi --algo infomap --graph karate
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value nmi --algo infomap --graph karate
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value nmi --algo infomap --graph karate
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value nmi --algo infomap --graph karate
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value nmi --algo infomap --graph karate
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value nmi --algo infomap --graph karate
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value nmi --algo infomap --graph karate
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value nmi --algo infomap --graph karate
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value nmi --algo infomap --graph karate
echo "Starting intra degree.."
python greedy.py --budget 4 --metric intraDegree --value nmi --algo infomap --graph karate

echo "Starting label_propagation.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value nmi --algo label_propagation --graph karate
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value nmi --algo label_propagation --graph karate
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value nmi --algo label_propagation --graph karate
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value nmi --algo label_propagation --graph karate
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value nmi --algo label_propagation --graph karate
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value nmi --algo label_propagation --graph karate
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value nmi --algo label_propagation --graph karate
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value nmi --algo label_propagation --graph karate
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value nmi --algo label_propagation --graph karate
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value nmi --algo label_propagation --graph karate
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value nmi --algo label_propagation --graph karate
echo "Starting intra degree.."
python greedy.py --budget 4 --metric intraDegree --value nmi --algo label_propagation --graph karate

echo "Starting leading_eigenvector.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value nmi --algo leading_eigenvector --graph karate
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value nmi --algo leading_eigenvector --graph karate
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value nmi --algo leading_eigenvector --graph karate
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value nmi --algo leading_eigenvector --graph karate
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value nmi --algo leading_eigenvector --graph karate
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value nmi --algo leading_eigenvector --graph karate
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value nmi --algo leading_eigenvector --graph karate
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value nmi --algo leading_eigenvector --graph karate
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value nmi --algo leading_eigenvector --graph karate
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value nmi --algo leading_eigenvector --graph karate
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value nmi --algo leading_eigenvector --graph karate
echo "Starting intra degree.."
python greedy.py --budget 4 --metric intraDegree --value nmi --algo leading_eigenvector --graph karate

echo "Starting multilevel.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value nmi --algo multilevel --graph karate
# echo "Starting local modularity"
python greedy.py --budget 4 --metric localMod --value nmi --algo multilevel --graph karate
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value nmi --algo multilevel --graph karate
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value nmi --algo multilevel --graph karate
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value nmi --algo multilevel --graph karate
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value nmi --algo multilevel --graph karate
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value nmi --algo multilevel --graph karate
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value nmi --algo multilevel --graph karate
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value nmi --algo multilevel --graph karate
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value nmi --algo multilevel --graph karate
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value nmi --algo multilevel --graph karate
echo "Starting intra degree.."
python greedy.py --budget 4 --metric intraDegree --value nmi --algo multilevel --graph karate

# echo "Starting spinglass.."
# python greedy.py --budget 4 --value nmi --algo spinglass

echo "Starting walktrap.."

echo "Starting clustering coefficient.."
python greedy.py --budget 4 --metric clusteringCoeff --value nmi --algo walktrap --graph karate
# echo "Starting local modularity"
# python greedy.py --budget 4 --metric localMod --value nmi --algo walktrap --graph karate
echo "Starting degree centrality.."
python greedy.py --budget 4 --metric degreeCenter --value nmi --algo walktrap --graph karate
echo "Starting betweenness centrality.."
python greedy.py --budget 4 --metric betweenCenter --value nmi --algo walktrap --graph karate
echo "Starting eigenvector centrality.."
python greedy.py --budget 4 --metric eigenCenter --value nmi --algo walktrap --graph karate
echo "Starting closeness centrality.."
python greedy.py --budget 4 --metric closeCenter --value nmi --algo walktrap --graph karate
echo "Starting coreness.."
python greedy.py --budget 4 --metric coreness --value nmi --algo walktrap --graph karate
echo "Starting diversity.."
python greedy.py --budget 4 --metric diversity --value nmi --algo walktrap --graph karate
echo "Starting eccentricity.."
python greedy.py --budget 4 --metric eccentricity --value nmi --algo walktrap --graph karate
echo "Starting constraint.."
python greedy.py --budget 4 --metric constraint --value nmi --algo walktrap --graph karate
echo "Starting closeness vitality.."
python greedy.py --budget 4 --metric closeVital --value nmi --algo walktrap --graph karate
echo "Starting intra degree.."
python greedy.py --budget 4 --metric intraDegree --value nmi --algo walktrap --graph karate