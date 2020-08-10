import json
import os

jname = "/data/kevinq/exps/1596299960.369978/output.json"
outname = "/data/kevinq/exps/1596299960.369978/output_mod.json"
js = json.load(open(jname,"r"))

new_dict = {}
event_list = []
with open("./labels_det.txt","r") as f:
    events = f.readlines()
for event in events:
    event_list.append(event.strip())
new_dict["filesProcessed"] = js["filesProcessed"]
new_dict["activities"] = []
print(len(js["filesProcessed"]))
acts = js["activities"]
for act in acts:
    act["activityID"] = event_list.index(act["activity"])
    new_dict["activities"].append(act)

json_str = json.dumps(new_dict,indent=4)
with open(outname, 'w') as save_json:
    save_json.write(json_str)