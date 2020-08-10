import csv
import json
import os

base_folder = "/home/kevinq/datasets/KF1_DET/props/experiments/MEVA-kitware_eo_s2-test_99-filtered_det"
jname = "/data/kevinq/exps/1596411799.810004/output_dir.json"


f = open("./labels_det.txt","r")
events = f.readlines()
event_dict = []
for event in events:
    event_dict.append(event.strip())

new_dict = {"filesProcessed":[],"activities":[]}
def load_labels(label_path):
    labels = {}
    csvfile = open(label_path,"r")
    reader = csv.reader(csvfile)
    for item in reader:
        if reader.line_num == 1:
            # print(item)
            continue
        label = list(map(float, item[2:]))
        assert len(label)==37
        labels[item[0]] = label
    return labels

prop_path = os.path.join(base_folder,"proposal")
label_path = os.path.join(base_folder,"label")
props = os.listdir(prop_path)

for prop in props:
    if prop.strip(".csv")+".avi" not in new_dict["filesProcessed"]:
        new_dict["filesProcessed"].append(prop.strip(".csv")+".avi")
    vid = prop.strip(".csv")+".avi"
    csvfile = open(os.path.join(prop_path,prop),"r")
    reader = csv.reader(csvfile)
    labels = load_labels(os.path.join(label_path,prop))
    for item in reader:
        if reader.line_num == 1:
            print(item)
            continue
        start = int(float(item[4]))
        end = int(float(item[5]))
        tid = int(float(item[1]))
        bbox = []
        for loc in item[6:]:
            bbox.append(int(float(loc)))
        assert len(bbox)==4
        assert len(event_dict)==len(labels[item[0]])
        for idx in range(len(event_dict)):
            activity = event_dict[idx]
            activityID = idx
            conf = labels[item[0]][idx]
            act = {
            "activity": activity,
            "presenceConf": conf,
            "localization": {
                vid: {
                    str(start): 1,
                    str(end): 0
                }
            },
            "activityID": idx}
            new_dict["activities"].append(act)


json_str = json.dumps(new_dict,indent=4)
with open(jname, 'w') as save_json:
    save_json.write(json_str) 



