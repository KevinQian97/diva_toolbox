import pandas as pd
import os
from tensorboardX import SummaryWriter

tf_dir = "./log"
log_dir = "/home/kevinq/repos/TSA_MEVA_REPO/tmp/TSA_DET_RGB_R2plus1D-152_avg_segment32_e15"
rnds = 3
csv_head = "log-rnd"
bst_epchs = [3,1,0]
tf_writer = SummaryWriter(log_dir=tf_dir)
trn_step = 0
tst_step = 0
for rnd in range(rnds):
    bst_epc = bst_epchs[rnd]
    csv_name = csv_head+str(rnd+1)+".csv"
    data = pd.read_csv(open(os.path.join(log_dir,csv_name),"r"))
    (num_row,num_col) = data.shape 
    print(num_row)
    for i in range(num_row):
        line = data.iloc[i]
        
        if "Test:" in line[0]:
            continue
        elif "Testing Results:" in line[0]:
            tst_prec1 = float(line[0].split("Prec@1 ")[1].split(" Prec@5")[0])
            tst_prec5 = float(line[0].split("Prec@5 ")[1].split(" Loss")[0])
            tst_loss = float(line[0].split("Loss ")[1].split(" nAUDC")[0])
            tst_naudc = float(line[0].split("nAUDC ")[1].split(" pMiss")[0])
            tst_pmiss = float(line[0].split("pMiss ")[1])
            tf_writer.add_scalar("tst/prec1",tst_prec1, tst_step)
            tf_writer.add_scalar("tst/prec5",tst_prec5, tst_step)
            tf_writer.add_scalar("tst/loss",tst_loss, tst_step)
            tf_writer.add_scalar("tst/nAUDC",tst_naudc, tst_step)
            tf_writer.add_scalar("tst/pMiss",tst_pmiss, tst_step)
            tst_step+=1
        elif "Epoch:" in line[0]:
            epc = int(line[0].split("]")[0].split("[")[-1])
            if epc>bst_epc:
                break
            trn_loss = float(line[1].split("Loss")[1].split(")")[0].split("(")[1])
            trn_prec1 = float(line[1].split("Prec@1")[1].split(")")[0].split("(")[1])
            trn_prec5 = float(line[1].split("Prec@5")[1].split(")")[0].split("(")[1])
            tf_writer.add_scalar("trn/prec1",trn_prec1, trn_step)
            tf_writer.add_scalar("trn/prec5",trn_prec5, trn_step)
            tf_writer.add_scalar("trn/loss",trn_loss, trn_step)        
            trn_step+=20
        else:
            continue



