import sys,os
sys.path.append(os.getcwd())
import argparse
import logging
from rumour_detection_module.model.Twitter.BiGCN_Twitter import Net
import torch
from torch_geometric.data import DataLoader
from rumour_detection_module.Process.rand5fold import *
from rumour_detection_module.Process.process import *
from rumour_detection_module.tools.evaluate import *
import os
import numpy as np 
from pathlib import Path
import torch.nn.functional as F
from tqdm import tqdm

logging.basicConfig(level=logging.DEBUG,
                    format='[%(filename)s:%(lineno)d] - %(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MODEL_CHECKPOINT_PATH = os.path.join(Path(
    os.path.abspath(__file__)).parent.parent,"rumour_detection_module","model","Twitter","model_weights")

def perform_concept_drift_test(model_weights: str, dataset_name: str, fold_train, fold_test, fold_num):
    """Perform concept drift test by evaluating pretrained model on dataset.

    Args:
        model_weights (str): Pretrained model name
        dataset_name (str): Name of dataset for concept drift test
        fold_train (_type_): Train fold data
        fold_test (_type_): Test fold data
        fold_num (_type_): Fold number

    Returns:
        Evaluation metrics obtained on the test set.
    """
    logger.info("Preparing pretrained model")
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = Net(5000, 64, 64).to(device)
    model.load_state_dict(torch.load(os.path.join(MODEL_CHECKPOINT_PATH,model_weights + "_" + str(fold_num))))
    model.eval()
    logger.info("Loaded")
    batchsize=128
    TDdroprate=0.2
    BUdroprate=0.2
    treeDic=loadTree(dataset_name)
    _, testdata_list = loadBiData(dataset_name, treeDic, fold_train, fold_test, TDdroprate,BUdroprate)
    test_loader = DataLoader(testdata_list, batch_size=batchsize, shuffle=True, num_workers=0)
    tqdm_test_loader = tqdm(test_loader)
    temp_val_losses = []
    temp_val_accs = []
    val_losses = []
    val_accs = []
    temp_val_Acc_all, temp_val_Acc1, temp_val_Prec1, temp_val_Recll1, temp_val_F1, \
    temp_val_Acc2, temp_val_Prec2, temp_val_Recll2, temp_val_F2, \
    temp_val_Acc3, temp_val_Prec3, temp_val_Recll3, temp_val_F3, \
    temp_val_Acc4, temp_val_Prec4, temp_val_Recll4, temp_val_F4 = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
    for Batch_data in tqdm_test_loader:
        Batch_data.to(device)
        val_out = model(Batch_data)
        val_loss  = F.nll_loss(val_out, Batch_data.y)
        temp_val_losses.append(val_loss.item())
        _, val_pred = val_out.max(dim=1)
        correct = val_pred.eq(Batch_data.y).sum().item()
        val_acc = correct / len(Batch_data.y)
        Acc_all, Acc1, Prec1, Recll1, F1, Acc2, Prec2, Recll2, F2, Acc3, Prec3, Recll3, F3, Acc4, Prec4, Recll4, F4 = evaluation4class(
            val_pred, Batch_data.y)
        temp_val_Acc_all.append(Acc_all), temp_val_Acc1.append(Acc1), temp_val_Prec1.append(
            Prec1), temp_val_Recll1.append(Recll1), temp_val_F1.append(F1), \
        temp_val_Acc2.append(Acc2), temp_val_Prec2.append(Prec2), temp_val_Recll2.append(
            Recll2), temp_val_F2.append(F2), \
        temp_val_Acc3.append(Acc3), temp_val_Prec3.append(Prec3), temp_val_Recll3.append(
            Recll3), temp_val_F3.append(F3), \
        temp_val_Acc4.append(Acc4), temp_val_Prec4.append(Prec4), temp_val_Recll4.append(
            Recll4), temp_val_F4.append(F4)
        temp_val_accs.append(val_acc)
    val_losses.append(np.mean(temp_val_losses))
    val_accs.append(np.mean(temp_val_accs))
    logger.info("Val_Loss {:.4f}| Val_Accuracy {:.4f}".format(np.mean(temp_val_losses), np.mean(temp_val_accs)))
    accs =np.mean(temp_val_accs)
    F1 = np.mean(temp_val_F1)
    F2 = np.mean(temp_val_F2)
    F3 = np.mean(temp_val_F3)
    F4 = np.mean(temp_val_F4)
    return accs,F1,F2,F3,F4

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights_name', dest = "weights_name", type=str, help = "Name of the pretrained model weights")
    parser.add_argument('--dataset_name', dest = "dataset_name", type=str, help = "Name of the dataset for testing")
    args = parser.parse_args()
    dataset_name = args.dataset_name
    fold0_x_test, fold0_x_train, \
    fold1_x_test,  fold1_x_train,  \
    fold2_x_test, fold2_x_train, \
    fold3_x_test, fold3_x_train, \
    fold4_x_test,fold4_x_train = load5foldData(dataset_name)

    # Simulate 5 Folds
    accs_0, F1_0, F2_0, F3_0, F4_0 = perform_concept_drift_test(args.weights_name, dataset_name, fold0_x_train, fold0_x_test, 0)
    accs_1, F1_1 ,F2_1 ,F3_1 ,F4_1 = perform_concept_drift_test(args.weights_name, dataset_name, fold1_x_train, fold1_x_test, 1)
    accs_2, F1_2, F2_2, F3_2, F4_2 = perform_concept_drift_test(args.weights_name, dataset_name, fold2_x_train, fold2_x_test, 2)
    accs_3, F1_3, F2_3, F3_3, F4_3 = perform_concept_drift_test(args.weights_name, dataset_name, fold3_x_train, fold3_x_test, 3)
    accs_4, F1_4, F2_4, F3_4, F4_4 = perform_concept_drift_test(args.weights_name, dataset_name, fold4_x_train, fold4_x_test, 4)
    test_accs = []
    NR_F1 = []
    FR_F1 = []
    TR_F1 = []
    UR_F1 = []
    test_accs.append((accs_0 + accs_1 + accs_2 + accs_3 +accs_4)/5)
    NR_F1.append((F1_0+F1_1+F1_2+F1_3+F1_4)/5)
    FR_F1.append((F2_0 + F2_1 + F2_2 + F2_3 + F2_4) / 5)
    TR_F1.append((F3_0 + F3_1 + F3_2 + F3_3 + F3_4) / 5)
    UR_F1.append((F4_0 + F4_1 + F4_2 + F4_3 + F4_4) / 5)
    logger.info("Total_Test_Accuracy: {:.4f}|NR F1: {:.4f}|FR F1: {:.4f}|TR F1: {:.4f}|UR F1: {:.4f}".format(
        sum(test_accs), sum(NR_F1), sum(FR_F1), sum(TR_F1), sum(UR_F1)))
