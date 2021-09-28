import os
import json
import csv

exp_dir = "/home/kevinq/exps/round3-filt"
call_path = "/home/kevinq/repos/ActEV_Scorer/ActEV_Scorer.py"
pred_path = "/home/kevinq/exps/round3-filt/output-filt-vis.json"
gt_path = "/home/kevinq/datasets/KF1_DET/reference/kitware_eo-all_257.json"
act_index = json.load(open(os.path.join(exp_dir,"activity-index.json"),"r"))
act_types = list(act_index.keys())
gt = json.load(open(gt_path,"r"))
pred = json.load(open(pred_path,"r"))
assert(len(gt["filesProcessed"])==len(pred["filesProcessed"]))

per_vid_gt = {}
per_vid_pred = {}

for f in gt["filesProcessed"]:
    os.makedirs(os.path.join(exp_dir,f))
    per_vid_gt[f] = []
    per_vid_pred[f] = []

gt_acts = gt["activities"]
pred_acts = pred["activities"]

for act in gt_acts:
    vid_name = list(act["localization"].keys())[0]
    per_vid_gt[vid_name].append(act)

for act in pred_acts:
    vid_name = list(act["localization"].keys())[0]
    per_vid_pred[vid_name].append(act)

for f,v in per_vid_gt.items():
    gt_dict = {"filesProcessed":[f],"activities":v}
    json_str = json.dumps(gt_dict,indent=4)
    with open(os.path.join(exp_dir,f,"gt.json"), 'w') as save_json:
        save_json.write(json_str)
    f_dict = {f:{"framerate":30.0,"selected":{"0":1,"9000":0}}}
    json_str = json.dumps(f_dict,indent=4)
    with open(os.path.join(exp_dir,f,"file-index.json"), 'w') as save_json:
        save_json.write(json_str)
    

for f,v in per_vid_pred.items():
    pred_dict = {"filesProcessed":[f],"activities":v,"processingReport":{"fileStatuses":{f:{'status': 'success', 'message': ''}}}}
    json_str = json.dumps(pred_dict,indent=4)
    with open(os.path.join(exp_dir,f,"pred.json"), 'w') as save_json:
        save_json.write(json_str) 

vid_wise_dict = {}
for f in gt["filesProcessed"]:
    vid_wise_dict[f] = {}
    s = os.path.join(exp_dir,f,"pred.json")
    r = os.path.join(exp_dir,f,"gt.json")
    a = os.path.join(exp_dir,"activity-index.json")
    i = os.path.join(exp_dir,f,"file-index.json")
    o = os.path.join(exp_dir,f)
    print("Start Calculatomg Pmiss and nAUDC for {}".format(f))
    call = "python {} ActEV_SDL_V2 -s {} -r {} -a {} -f {} -o {} -v -n 4".format(call_path,s,r,a,i,o)
    os.system(call)
    csvFile = open(os.path.join(exp_dir,f,"scores_aggregated.csv"),"r")
    reader = csv.reader(csvFile)
    for item in reader:
        if "mean-nAUDC@0.2tfa" in item[0]:
            nAUDC = float(item[0].split("|")[-1])
        if "mean-p_miss@0.02tfa" in item[0]:
            pMiss = float(item[0].split("|")[-1])
    vid_wise_dict[f]["nAUDC"]=nAUDC
    vid_wise_dict[f]["pMiss"]=pMiss
    csvFile = open(os.path.join(exp_dir,f,"scores_by_activity.csv"),"r")
    reader = csv.reader(csvFile)
    for item in reader:
        if "|nAUDC@0.2tfa|" in item[0]:
            act_type = item[0].split("|")[0]
            nAUDC = float(item[0].split("|")[-1])
            if act_type not in vid_wise_dict[f]:
                vid_wise_dict[f][act_type] = {}
            vid_wise_dict[f][act_type]["nAUDC"] = nAUDC
        if "|p_miss@0.02tfa|" in item[0]:
            act_type = item[0].split("|")[0]
            pMiss = float(item[0].split("|")[-1])
            if act_type not in vid_wise_dict[f]:
                vid_wise_dict[f][act_type] = {}
            vid_wise_dict[f][act_type]["pMiss"] = pMiss

for f in list(vid_wise_dict.keys()):
    acts = json.load(open(os.path.join(exp_dir,f,"pred.json"),"r"))["activities"]
    for act in acts:
        act_type = act["activity"]
        if act_type not in vid_wise_dict[f]:
            continue
        if "num" not in vid_wise_dict[f][act_type]:
            vid_wise_dict[f][act_type]["num"]=0
        vid_wise_dict[f][act_type]["num"]+=1


json_str = json.dumps(vid_wise_dict,indent=4)
with open(os.path.join(exp_dir,"res.json"), 'w') as save_json:
    save_json.write(json_str) 



