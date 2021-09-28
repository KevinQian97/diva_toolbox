import json
import os

thresh_dict = json.load(open("./thresh.json","r"))
pred = json.load(open("/home/kevinq/exps/round3/output_mod.json","r"))
filt_dict = {"filesProcessed":pred["filesProcessed"],"activities":[],"processingReport":pred["processingReport"]}
acts = pred["activities"]
for act in acts:
    if act["activity"] in thresh_dict and act["presenceConf"]>=thresh_dict[act["activity"]]:
        filt_dict["activities"].append(act)

json_str = json.dumps(filt_dict,indent=4)
with open(os.path.join("/home/kevinq/exps/round3","output-filt-vis.json"), 'w') as save_json:
    save_json.write(json_str) 
