import json
import os
import numpy as np
import csv

js = json.load(open("/home/kevinq/datasets/STR/pip_250k_stabilized_nomevapad_annotations/str250k_annot.json"))
db = js["database"]
act_wise_count = [0]*37

for k,v in db.items():
    conf = v["annotations"]["conf"]
    for i in range(37):
        if conf[i]:
            act_wise_count[i]+=1

with open("./str_actwise_count.csv",'w') as f:
    csv_write = csv.writer(f)
    csv_write.writerow(act_wise_count)

