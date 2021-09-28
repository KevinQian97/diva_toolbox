import json
import os
res_fold = "/home/kevinq/exps/round3-filt"
res_dict = json.load(open(os.path.join(res_fold,"res.json"),"r"))
rank_dict = {"nAUDC":{"vids":[],"scores":[]},"pMiss":{"vids":[],"scores":[]}}
per_act_num_thres = 5
avg_num_thres = 20

for k,v in res_dict.items():
    v_num = 0
    for metric,score in v.items():
        if metric in ["nAUDC","pMiss"]:
            continue
        if "num" in score:
            v_num+=score["num"]
    res_dict[k]["num"] = v_num

for k,v in res_dict.items():
    for metric,score in v.items():
        if metric == "num":
            continue
        if metric in ["nAUDC","pMiss"]:  
            if score>=0 and "num" in res_dict[k] and res_dict[k]["num"]>avg_num_thres:
                rank_dict[metric]["vids"].append(k)
                rank_dict[metric]["scores"].append(score)
        else:
            if metric+"-nAUDC" not in rank_dict:
                rank_dict[metric+"-nAUDC"] = {"vids":[],"scores":[]}
                rank_dict[metric+"-pMiss"] = {"vids":[],"scores":[]}
            if "num" in score and score["num"]>per_act_num_thres:
                if score["nAUDC"] >=0:
                    rank_dict[metric+"-nAUDC"]["vids"].append(k)
                    rank_dict[metric+"-nAUDC"]["scores"].append(score["nAUDC"])
                if score["pMiss"] >=0:
                    rank_dict[metric+"-pMiss"]["vids"].append(k)
                    rank_dict[metric+"-pMiss"]["scores"].append(score["pMiss"])
    

sort_dict = {}
for metric,info in rank_dict.items():
    if len(info["vids"]):
        sort_zipped = sorted(zip(info["scores"],info["vids"]))
        result = zip(*sort_zipped)
        _,sort_dict[metric] = [list(x)for x in result]

json_str = json.dumps(sort_dict,indent=4)
with open(os.path.join(res_fold,"sort.json"), 'w') as save_json:
    save_json.write(json_str) 



