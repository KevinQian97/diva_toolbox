import json
import os
from multiprocessing import Pool

dataset = "MEVA"
base_path = "/home/data/exps/1620060644.3474147"
json_path = os.path.join(base_path,"output.json")
act_path = os.path.join(base_path,"activity-index.json")
output_folder = os.path.join(base_path,"event-wise")
scorer_path = "/home/kevinq/repos/ActEV_Scorer"
ref_path = "/home/kevinq/exps/kf1_test_s2.json"
n_jobs = 64
is_filt = False
if is_filt:
    filt_dict = json.load(open("./event_thresh.json","r"))
is_calc = False


def actev_scorer_api(command):
    print(command)
    # raise RuntimeError("stop")
    os.system(command)

def prepare_commands(ref_path,base_path,output_folder,scorer_path,events):
    commands = []
    for event in events:
        path = os.path.join(output_folder,event)
        command = "python {}/ActEV_Scorer.py ActEV_SDL_V2 -s {}/output.json -r {} -a {}/activity-index.json -f {}/file-index.json -o {}".format(scorer_path.strip("\n"),\
            path.strip("\n"),ref_path.strip("\n"),path.strip("\n"),base_path.strip("\n"),path.strip("\n"))
        commands.append(command)
    return commands


print("start prepare event-wise files")
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
js = json.load(open(json_path,"r")) 
filesProcessed = js["filesProcessed"]
activities = js["activities"]
acts_index = json.load(open(act_path,"r"))
if dataset=="MEVA":
    f = open("./labels.txt","r")
else:
    f = open("./labels_virat.txt","r")
events = f.readlines()
event_list = []
for event in events:
    event_list.append(event.strip())
event_dict = {}
for event in event_list:
    event_dict[event] = []
for act in activities:
    if is_filt:
        if act["presenceConf"] > filt_dict[act["activity"]]["conf_thresh"]:
            event_dict[act["activity"]].append(act)
    else:
        event_dict[act["activity"]].append(act)

for event in event_list:
    if not os.path.exists(os.path.join(output_folder,event)):
        os.makedirs(os.path.join(output_folder,event))
    jname = "output.json"
    new_dict = {}
    new_dict["filesProcessed"] = filesProcessed
    new_dict["activities"] = event_dict[event]
    json_str = json.dumps(new_dict,indent=4)
    with open(os.path.join(output_folder,event,jname), 'w') as save_json:
        save_json.write(json_str)
    jname = "activity-index.json"
    new_dict = {}
    new_dict[event] = acts_index[event]
    json_str = json.dumps(new_dict,indent=4)
    with open(os.path.join(output_folder,event,jname), 'w') as save_json:
        save_json.write(json_str)    

print("successfully prepare json files")
if is_calc:
    commands = prepare_commands(ref_path,base_path,output_folder,scorer_path,events)

    print("start scorer")
    pool = Pool(n_jobs)
    pool.map(actev_scorer_api, commands)
    pool.close()


