import os
import csv

input_path = "/mnt/cache/exps/1619759302.8884728/scores_by_activity.csv"
out_path = "./output.csv"


def create_csv():
    path = "aa.csv"
    with open(path,'wb') as f:
        csv_write = csv.writer(f)
        csv_head = ["good","bad"]
        csv_write.writerow(csv_head)

indexes = ["nAUDC@0.2tfa","p_miss@0.02tfa"]


res_dict = {}
with open(input_path,"r") as f:
    csv_read = csv.reader(f)
    for line in csv_read:
        line = line[0].strip()
        for idx in indexes:
            if idx in line:
                print(line)
                [act,_,score] = line.split("|")
                if act not in res_dict:
                    res_dict[act] = {}
                res_dict[act][idx] = score
g = open(out_path,'w')
csv_write = csv.writer(g)
csv_write.writerow(["Activity","nAUDC@0.2tfa","p_miss@0.02tfa"])
for k,v in res_dict.items():
    csv_write.writerow([k,v["nAUDC@0.2tfa"],v["p_miss@0.02tfa"]])


