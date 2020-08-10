import os
import json

js = json.load(open("/data/kevinq/exps/1596299960.369978/output.json","r"))
findex = list(json.load(open("/data/kevinq/exps/1596299960.369978/file-index.json")).keys())
jname = "/data/kevinq/exps/1596299960.369978/output_mod.json"
new_dict = {}
new_dict["filesProcessed"] = findex
new_dict["activities"] = js["activities"]
# print(new_dict["filesProcessed"])
json_str = json.dumps(new_dict,indent=4)
with open(jname, 'w') as save_json:
    save_json.write(json_str)