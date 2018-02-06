#!/bin/bash

echo "Starting nmi value.."

echo "Starting louvain.."

echo "Starting clustering coefficient.."
python community_attack.py --budget 4 --glo_metric link_density --com_metric clusteringCoeff --value nmi --algo louvain --graph karate
# echo "Starting local nmi"
# python community_attack.py --budget 4 --glo_metric link_density --com_metric localMod --value nmi --algo louvain --graph karate
echo "Starting degree centrality.."
python community_attack.py --budget 4 --glo_metric link_density --com_metric degreeCenter --value nmi --algo louvain --graph karate
echo "Starting betweenness centrality.."
python community_attack.py --budget 4 --glo_metric link_density --com_metric betweenCenter --value nmi --algo louvain --graph karate
echo "Starting eigenvector centrality.."
python community_attack.py --budget 4 --glo_metric link_density --com_metric eigenCenter --value nmi --algo louvain --graph karate
echo "Starting closeness centrality.."
python community_attack.py --budget 4 --glo_metric link_density --com_metric closeCenter --value nmi --algo louvain --graph karate
echo "Starting coreness.."
python community_attack.py --budget 4 --glo_metric link_density --com_metric coreness --value nmi --algo louvain --graph karate
echo "Starting diversity.."
python community_attack.py --budget 4 --glo_metric link_density --com_metric diversity --value nmi --algo louvain --graph karate
echo "Starting eccentricity.."
python community_attack.py --budget 4 --glo_metric link_density --com_metric eccentricity --value nmi --algo louvain --graph karate
echo "Starting constraint.."
python community_attack.py --budget 4 --glo_metric link_density --com_metric constraint --value nmi --algo louvain --graph karate
echo "Starting closeness vitality.."
python community_attack.py --budget 4 --glo_metric link_density --com_metric closeVital --value nmi --algo louvain --graph karate
echo "Starting intra degree.."
python community_attack.py --budget 4 --glo_metric link_density --com_metric intraDegree --value nmi --algo louvain --graph karate
echo "Stating myNMI.."
python community_attack.py --budget 4 --glo_metric link_density --com_metric myNMI --value nmi --algo louvain --graph karate
# echo "Starting myMod.."
# python community_attack.py --budget 4 --glo_metric link_density --com_metric myMod --value nmi --algo louvain --graph karate

echo "Done!!"