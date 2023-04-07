from pathlib import Path
import os
import argparse
import random

TWITTER_15_PATH = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "data", "Twitter15", "data.TD_RvNN.vol_5000.txt")
TWITTER_15_LABEL_PATH = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "data", "Twitter15", "Twitter15_label_All.txt")

TWITTER_16_PATH = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "data", "Twitter16", "data.TD_RvNN.vol_5000.txt")
TWITTER_16_LABEL_PATH = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "data", "Twitter16", "Twitter16_label_All.txt")

NEW_DATA_PATH = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "data", "Twitter15_16_Mix", "data.TD_RvNN.vol_5000.txt")
NEW_DATA__LABEL_PATH = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "data", "Twitter15_16_Mix", "Twitter15_16_Mix_label_All.txt")

TWITTER15_CHOICE_PATH = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "data", "Twitter15_PORT", "data.TD_RvNN.vol_5000.txt")
TWITTER15_CHOICE__LABEL_PATH = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "data", "Twitter15_PORT", "Twitter15_PORT_label_All.txt")

NEW_DATA_PATH = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "data", "Twitter15_16_Mix", "data.TD_RvNN.vol_5000.txt")
NEW_DATA__LABEL_PATH = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "data", "Twitter15_16_Mix", "Twitter15_16_Mix_label_All.txt")

TWITTER16_CHOICE_PATH = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "data", "Twitter16_PORT", "data.TD_RvNN.vol_5000.txt")
TWITTER16_CHOICE__LABEL_PATH = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "data", "Twitter16_PORT", "Twitter16_PORT_label_All.txt")
 
TWITTER15_LEFTOVER_PATH = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "data", "Twitter15_LO", "data.TD_RvNN.vol_5000.txt")
TWITTER15_LEFTOVER__LABEL_PATH = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "data", "Twitter15_LO", "Twitter15_LO_label_All.txt")

TWITTER16_LEFTOVER_PATH = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "data", "Twitter16_LO", "data.TD_RvNN.vol_5000.txt")
TWITTER16_LEFTOVER__LABEL_PATH = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "data", "Twitter16_LO", "Twitter16_LO_label_All.txt")

def mix_datasets(mix_amount_15, mix_amount_16):
    """Randomly mix Twitter15 and Twitter16 datasets according to certain proportions of each.

    Args:
        mix_amount_15 (float): The amount of Twitter15 data to mix.
        mix_amount_16 (float): The amount of Twitter16 data to mix.
    """
    twitter15_data, twitter15_labels = load_dataset_information(TWITTER_15_PATH, TWITTER_15_LABEL_PATH)
    twitter16_data, twitter16_labels = load_dataset_information(TWITTER_16_PATH, TWITTER_16_LABEL_PATH)

    twitter15_ids = list(twitter15_data.keys())
    twitter16_ids = list(twitter16_data.keys())

    # Choose new Twitter15 ids.
    chosen_twitter15_ids = []
    for _ in range(round(len(twitter15_ids)*mix_amount_15)):
        choice = random.choice(twitter15_ids)
        twitter15_ids.remove(choice)
        chosen_twitter15_ids.append(choice)
    
    # Choose new Twitter16 ids.
    chosen_twitter16_ids = []
    for _ in range(round(len(twitter16_ids)*mix_amount_16)):
        choice = random.choice(twitter16_ids)
        twitter16_ids.remove(choice)
        chosen_twitter16_ids.append(choice)
    
    print("Chosen Twitter15", len(chosen_twitter15_ids))
    print("Chosen Twitter16", len(chosen_twitter16_ids))
    print("Combined", len(chosen_twitter15_ids) + len(chosen_twitter16_ids))
    print("Leftover", len(twitter15_ids))
    print("Leftover", len(twitter16_ids))

    # Write Twitter15 portion.
    write_cascade_and_labels(chosen_twitter15_ids, NEW_DATA__LABEL_PATH, NEW_DATA_PATH, twitter15_labels, twitter15_data)
    write_cascade_and_labels(chosen_twitter15_ids, TWITTER15_CHOICE__LABEL_PATH, TWITTER15_CHOICE_PATH, twitter15_labels, twitter15_data)
    # Write Twitter16 portion.
    write_cascade_and_labels(chosen_twitter16_ids, NEW_DATA__LABEL_PATH, NEW_DATA_PATH, twitter16_labels, twitter16_data)
    write_cascade_and_labels(chosen_twitter16_ids, TWITTER16_CHOICE__LABEL_PATH, TWITTER16_CHOICE_PATH, twitter16_labels, twitter16_data)
    # Write Twitter15 leftover
    write_cascade_and_labels(twitter15_ids, TWITTER15_LEFTOVER__LABEL_PATH, TWITTER15_LEFTOVER_PATH, twitter15_labels, twitter15_data)
    # Write Twitter16 leftover
    write_cascade_and_labels(twitter16_ids, TWITTER16_LEFTOVER__LABEL_PATH, TWITTER16_LEFTOVER_PATH, twitter16_labels, twitter16_data)


def write_cascade_and_labels(eids, label_path, cascade_path, labels, cascade):
    """Function to write the new cascade data file and new label file.

    Args:
        eids (list): List of tweet ids to be included in dataset.
        label_path (str): Path to the dataset labels.
        cascade_path (str): Path to the dataset cascade.
        labels (dict): Dictionary mapping tweet ids to labels.
        cascade (dict): Dictionary mapping tweet ids to cascades.
    """
    for eid in eids:
        with open(label_path, mode="a") as f:
            f.write(labels[eid] + "\t" + "<PLACE>" + "\t" + eid + "\n")

        with open(cascade_path, mode="a") as f:
            for line in cascade[eid]:
                f.write(line + "\n")

def load_dataset_information(data_path, label_path):
    """Load in dataset files

    Args:
        data_path (str): Path to the data file.
        label_path (str): Path to the label file

    Returns:
        dict, dict: Two dictionaries. The first mapping the tweet id to its cascade,
        the second mapping the tweet id to its corresponding id.
    """
    ids2cascade = {}
    for line in open(data_path):
        line = line.rstrip()
        eid, _, _ = line.split('\t')[0], line.split('\t')[1], int(line.split('\t')[2])
        if eid not in ids2cascade:
            ids2cascade[eid] = [line]
        else:
            ids2cascade[eid].append(line)

    labels = {}
    for line in open(label_path):
        line = line.rstrip()
        label, eid = line.split('\t')[0], line.split('\t')[2]
        label=label.lower()
        if eid in labels:
            raise KeyError("There shouldn't be a double label")
        else:
            labels[eid] = label
    return ids2cascade, labels

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mix_amount_15', dest = "mix_amount_15", type=float, help = "The number of examples to be selected from Twitter15")
    parser.add_argument('--mix_amount_16', dest = "mix_amount_16", type=float, help = "The number of examples to be selected from Twitter16")
    args = parser.parse_args()
    mix_amount_15 = float(args.mix_amount_15)
    mix_amount_16 = float(args.mix_amount_16)
    if (mix_amount_15 + mix_amount_16) != 1:
        raise ValueError("The two mix amounts provided need to some to 1")
    mix_datasets(mix_amount_15, mix_amount_16)