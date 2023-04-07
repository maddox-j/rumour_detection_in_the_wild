import os
from pathlib import Path 
import argparse
import numpy as np

class Node:
    """Class used to represent a node in the Tweet cascade.
    """
    def __init__(self, eid, indexP, indexC, max_degree, maxL, Vec):
        self.eid = eid
        self.indexP = indexP
        self.indexC = indexC
        self.max_degree = max_degree
        self.maxL = maxL
        self.Vec = Vec
        self.parent_pointer = None
        self.deleted = None

def perform_node_ablation(dataset, drop_amount):
    """Generate node ablated dataset

    Args:
        dataset (str): The dataset on which to perform node ablation.
        drop_amount (float): Per cascade, the percentage at which we ablate nodes.
    """
    treePath = os.path.join(Path(os.path.abspath(__file__)).parent.parent, 'data/' + dataset + '/data.TD_RvNN.vol_5000.txt')
    new_dataset_name = dataset + "_edges_" + str(drop_amount)
    new_tree_path = os.path.join(Path(os.path.abspath(__file__)).parent.parent, 'data/' + new_dataset_name  + '/data.TD_RvNN.vol_5000.txt')
    eid_cache = []
    current_eid = None
    for line in open(treePath):
        line = line.rstrip()
        eid, indexP, indexC = line.split('\t')[0], line.split('\t')[1], int(line.split('\t')[2])
        max_degree, maxL, Vec = int(line.split('\t')[3]), int(line.split('\t')[4]), line.split('\t')[5]
        if current_eid is None:
            current_eid = eid
            eid_cache.append(Node(eid, indexP, indexC, max_degree, maxL, Vec))
        elif current_eid == eid:
            eid_cache.append(Node(eid, indexP, indexC, max_degree, maxL, Vec))
        elif eid != current_eid:
            drop_and_write(eid_cache, drop_amount, new_tree_path)
            eid_cache = []
            current_eid = eid
            eid_cache.append(Node(eid, indexP, indexC, max_degree, maxL, Vec))
               
def drop_and_write(eid_cache, drop_amount, new_tree_path):
    """Drop nodes from a particular tweet cascade, and write the resultant cascade
    to a file.

    Args:
        eid_cache (list): Cache of the current nodes in the tweet cascade.
        drop_amount (float): The percentage at which nodes are dropped from the cascade.
        new_tree_path (string): The path for the new dataset.
    """
    eid_cache = sorted(eid_cache, key=lambda x: x.indexC)
    for idx, i in enumerate(eid_cache):
        # Ignore the root.
        if i.indexP != "None":
            # The data does used zero based counts. Establish pointer
            i.parent_pointer = eid_cache[int(i.indexP)-1]
            assert int(i.indexP) == int(i.parent_pointer.indexC)
            if np.random.binomial(1, drop_amount):
                i.deleted = True
    new_eid_cache = []
    deleted_nodes = []
    # Start removing deleted.
    for i in eid_cache:
        if i.deleted:
            deleted_nodes.append(i)
            continue
        if i.parent_pointer in deleted_nodes:
            i.deleted = True
            deleted_nodes.append(i)
            continue
        new_eid_cache.append(i)
    
    # Reassign idx.
    for idx, i in enumerate(new_eid_cache):
        i.indexC = idx + 1
        if i.indexP != "None":  
            i.indexP = (i.parent_pointer.indexC)
        with open(new_tree_path, mode = "a") as f:
            line_to_write = i.eid + "\t" + str(i.indexP) + "\t" + str(i.indexC) + "\t" + str(i.max_degree) + "\t" + str(i.maxL) + "\t" + i.Vec
            f.write(line_to_write + "\n")

            
if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--drop_amount', dest = "drop_amount", type=float, help = "The probability at which edges should be dropped.")
    parser.add_argument('--dataset_name', dest = "dataset_name", type=str, help = "Name of the dataset for testing")
    args = parser.parse_args()
    drop_amount = args.drop_amount
    dataset = str(args.dataset_name)
    perform_node_ablation(dataset,drop_amount)