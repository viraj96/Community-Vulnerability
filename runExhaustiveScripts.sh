#!/bin/bash

echo "Starting karate network.."

echo "Starting modularity metric.."

echo "Starting louvain.."
python exhaustiveAll.py --budget 4 --value modularity --algo louvain --graph karate

echo "Starting edge_betweenness.."
python exhaustiveAll.py --budget 4 --value modularity --algo edge_betweenness --graph karate

echo "Starting fast_greedy.."
python exhaustiveAll.py --budget 4 --value modularity --algo fast_greedy --graph karate

echo "Starting infomap.."
python exhaustiveAll.py --budget 4 --value modularity --algo infomap --graph karate

echo "Starting label_propagation.."
python exhaustiveAll.py --budget 4 --value modularity --algo label_propagation --graph karate

echo "Starting leading_eigenvector.."
python exhaustiveAll.py --budget 4 --value modularity --algo leading_eigenvector --graph karate

echo "Starting multilevel.."
python exhaustiveAll.py --budget 4 --value modularity --algo multilevel --graph karate

echo "Starting walktrap.."
python exhaustiveAll.py --budget 4 --value modularity --algo walktrap --graph karate