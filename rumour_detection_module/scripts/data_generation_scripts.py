import argparse
import numpy as np
import os
from pathlib import Path
from node_ablation_test import perform_node_ablation

def generate_dropped_graph(dataset, drop_amount, type_ablate):
    """Method to generate datasets for ablation experiments.

    Args:
        dataset (str): Path to dataset.
        drop_amount (float): The amount at which data abalation should occur.
        type_ablate (str): The type of ablation taht should occur.
    """
    if type_ablate == "text":
        treePath = os.path.join(Path(os.path.abspath(__file__)).parent.parent, 'data/' + dataset + '/data.TD_RvNN.vol_5000.txt')
        new_dataset_name = dataset + "_text_" + str(drop_amount)
        new_tree_path = os.path.join(Path(os.path.abspath(__file__)).parent.parent, 'data/' + new_dataset_name  + '/data.TD_RvNN.vol_5000.txt')
        for line in open(treePath):
            line = line.rstrip()
            eid, indexP, indexC = line.split('\t')[0], line.split('\t')[1], int(line.split('\t')[2])
            max_degree, maxL, Vec = int(line.split('\t')[3]), int(line.split('\t')[4]), line.split('\t')[5]
            if np.random.binomial(1, drop_amount):
                Vec = "0:1"
            with open(new_tree_path, mode = "a") as f:
                line_to_write = eid + "\t" + str(indexP) + "\t" + str(indexC) + "\t" + str(max_degree) + "\t" + str(maxL) + "\t" + Vec
                f.write(line_to_write + "\n")

    elif type_ablate == "edges":
        # Moved to other script for ease of reading.
        perform_node_ablation(dataset, drop_amount)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--drop_amount', dest = "drop_amount", type=float, help = "The probability at which edges should be dropped.")
    parser.add_argument('--dataset_name', dest = "dataset_name", type=str, help = "Name of the dataset for testing")
    parser.add_argument('--type', dest = "type", type=str, help = "Type of ablation")
    args = parser.parse_args()
    dataset = args.dataset_name
    drop_amount = args.drop_amount
    type_ablate = args.type
    generate_dropped_graph(dataset, drop_amount, type_ablate)

