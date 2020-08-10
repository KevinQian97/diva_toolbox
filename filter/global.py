import os
import json
base_path = "/data/kevinq/exps/1596864516.976852"
event_path = os.path.join(base_path,"event-wise")
findex = list(json.load(open(os.path.join(base_path,"file-index.json"),"r")).keys())


events = os.listdir(event_path)
loc = int(100*9000/64*0.4)

new_dict = {"filesProcessed":[],"activities":[]}
for event in events:
    rank_list = []
    js = json.load(open(os.path.join(event_path,event,"output.json")))
    acts  = js["activities"]
    print("Now tackle Event:{}".format(event))
    print(len(acts))
    for act in acts:
        rank_list.append(act["presenceConf"])
    rank_list.sort()
    score = rank_list[-loc]
    for act in acts:
        if act["presenceConf"] >= score:
            new_dict["activities"].append(act)

new_dict["filesProcessed"] = findex

json_str = json.dumps(new_dict,indent=4)
with open(os.path.join(base_path,"output_mod.json"), 'w') as save_json:
    save_json.write(json_str) 



    
    


