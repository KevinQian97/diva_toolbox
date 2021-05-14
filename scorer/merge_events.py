import csv
import os
import json
base_path = "/home/kevinq/exps"
path = os.path.join(base_path,"event-wise")
jname = os.path.join(base_path,"grap.json")
events = os.listdir(path)
events.sort()
targets = ["mean-nAUDC@0.2tfa","mean-p_miss@0.02tfa"]
new_dict = {}
for event in events:
    new_dict[event] = {}
    csvFile = open(os.path.join(path,event,"scores_aggregated.csv"),"r")
    reader = csv.reader(csvFile)
    for item in reader:
        k,v = item[0].split("|")
        if k in targets:
            new_dict[event][k] = float(v)

count_targets = [0,0]
score_targets = [0,0]

for event in events:
    for target in targets:
        if target in list(new_dict[event].keys()):
            count_targets[targets.index(target)]+=1
            score_targets[targets.index(target)]+=new_dict[event][target]

print(count_targets)
print(score_targets)
for target in targets:
    new_dict[target] = score_targets[targets.index(target)]/count_targets[targets.index(target)]


print(new_dict)
json_str = json.dumps(new_dict,indent=4)
with open(jname, 'w') as save_json:
    save_json.write(json_str)

