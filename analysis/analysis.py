import os
import json

ref_path = "/home/kevinq/datasets/KF1_DET/referemce"
act_dict = {}
label_file = open("/home/kevinq/datasets/KF1_DET/labels.txt","r")
lines = label_file.readlines()
label_list = []
temp_list = [32,64,128,256]
for line in lines:
    label_list.append(line.strip())
annots = os.listdir(ref_path)
act_dict["general"] = {"temporal-bound":[0,0,0,0,0]}
for label in label_list:
    act_dict[label] = {"trn_num":0,"trn_pos":0,"trn_neg":0,"tst_num":0,"tst_pos":0,"tst_neg":0,"temporal-bound":[0,0,0,0,0]}
for annot in annots:
    js = json.load(open(os.path.join(ref_path,annot)))
    db = js["activities"]
    for act in db:
        if act["activity"] not in act_dict:
            act_dict[act["activity"]] = {"trn_num":0,"trn_pos":0,"trn_neg":0,"tst_num":0,"tst_pos":0,"tst_neg":0,"temporal-bound":[0,0,0,0,0]}
        vid = list(act["localization"].keys())[0]
        [start,end] = act["localization"][vid].keys()
        start = int(start)
        end = int(end)
        temp_len = end-start
        if temp_len < 0:
            temp_len = -temp_len
        
        if temp_len<=32:
            act_dict[act["activity"]]["temporal-bound"][0]+=1
            act_dict["general"]["temporal-bound"][0]+=1
        elif temp_len<=64:
            act_dict[act["activity"]]["temporal-bound"][1]+=1
            act_dict["general"]["temporal-bound"][1]+=1
        elif temp_len<=128:
            act_dict[act["activity"]]["temporal-bound"][2]+=1
            act_dict["general"]["temporal-bound"][2]+=1
        elif temp_len<=256:
            act_dict[act["activity"]]["temporal-bound"][3]+=1
            act_dict["general"]["temporal-bound"][3]+=1
        else:
            act_dict[act["activity"]]["temporal-bound"][4]+=1
            act_dict["general"]["temporal-bound"][4]+=1
            
        
        if "train" in annot:
            act_dict[act["activity"]]["trn_num"]+=1
        else:
            act_dict[act["activity"]]["tst_num"]+=1

hit_path = "/home/kevinq/datasets/KF1_DET"
hit_files = ["kf1_test_anno_lijun_iod.json","kf1_train_anno_lijun_iod.json"]
for hit_file in hit_files:
    db = json.load(open(os.path.join(hit_path,hit_file),"r"))["database"]
    for k,v in db.items():
        if v["pos"] and v["pos"]!="STR":
            for i in range(37):
                if v["annotations"]["conf"][i] >0:
                    if "train" in hit_file:
                        act_dict[label_list[i]]["trn_pos"] +=1
                    else:
                        act_dict[label_list[i]]["tst_pos"] +=1
                else:
                    if "train" in hit_file:
                        act_dict[label_list[i]]["trn_neg"] +=1
                    else:
                        act_dict[label_list[i]]["tst_neg"] +=1

json_str = json.dumps(act_dict,indent=4)
with open("anlysis.json", 'w') as save_json:
    save_json.write(json_str)



