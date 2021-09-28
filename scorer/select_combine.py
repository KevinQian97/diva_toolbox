import csv
import os
from itertools import combinations
import numpy as np
import pandas as pd
import json

sys_num = 20
select_num = 3
class_num = 37
target = "metric_value"
csv_path = "/home/kevinq/repos/diva_toolbox/scorer/scores_by_activity.csv"
act_list = ['hand_interacts_with_person', 'person_abandons_package', 'person_carries_heavy_object', 'person_closes_facility_door', 'person_closes_trunk', 'person_closes_vehicle_door', 'person_embraces_person', 'person_enters_scene_through_structure', 'person_exits_scene_through_structure', 'person_exits_vehicle', 'person_enters_vehicle', 'person_interacts_with_laptop', 'person_loads_vehicle', 'person_opens_facility_door', 'person_opens_trunk', 'person_opens_vehicle_door', 'person_picks_up_object', 'person_purchases', 'person_puts_down_object', 'person_reads_document', 'person_rides_bicycle', 'person_sits_down', 'person_steals_object', 'person_stands_up', 'person_talks_on_phone', 'person_talks_to_person', 'person_texts_on_phone', 'person_transfers_object', 'person_unloads_vehicle', 'vehicle_drops_off_person', 'vehicle_picks_up_person', 'vehicle_makes_u_turn', 'vehicle_reverses', 'vehicle_starts', 'vehicle_stops', 'vehicle_turns_left',"vehicle_turns_right"]

def select(groups,db):
# db sys_num*37
    ans = {"val":np.inf, "group":[]}
    for group in groups:
        candidate = db[list(group)]
        val = np.sum(candidate.min(0))
        if val<ans["val"]:
            ans["val"] = val
            ans["group"] = group
    return ans

def gen_db(csv_path,target,class_num):
    db = {}
    df = pd.read_csv(csv_path)
    for index in df.index:
        row = df.loc[index]
        if row["submission_id"] not in db:
            db[row["submission_id"]] = np.zeros(class_num)
        db[row["submission_id"]][act_list.index(row["activity"])]=row[target]
    
    systems = list(db.keys())
    sys_num = len(systems)
    db_array = np.zeros((sys_num,class_num))
    for i in range(sys_num):
        db_array[i] = db[systems[i]]
    
    return db_array,systems

db,systems = gen_db(csv_path,target,class_num)
np.save("./db.npy",db)
print(systems)
# print(db)
groups = list(combinations(list(np.arange(sys_num)), select_num))
res = select(groups,db)
print("min target: {}".format(res["val"]/class_num))

candid = db[list(res["group"])]
optim_score = candid.min(0)
select_dict = {}

for idx in res["group"]:
    select_dict[int(systems[idx])] = []
    score = db[idx]
    for i in range(len(act_list)):
        if score[i] == optim_score[i]:
            select_dict[int(systems[idx])].append(act_list[i])
    print(systems[idx])

json_str = json.dumps(select_dict,indent=4)
with open("./select.json", 'w') as save_json:
    save_json.write(json_str)








