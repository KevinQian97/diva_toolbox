import json
import os

# k1_cats = ["person_carries_object","person_enters_facility_or_vehicle", \
#         "person_pushs_object","person_stands","person_talks_on_phone", \
#         "vehicle_makes_u_turn","vehicle_moves","vehicle_starts","vehicle_stops"]

# k2_cats = ["person_crouches","person_enters_facility_or_vehicle","person_pushs_object", \
#         "person_runs","person_gestures","person_pickups_object"]

# k3_cats = ["person_carries_object","person_enters_facility_or_vehicle","person_pushs_object", \
# "person_stands","vehicle_drops_off_person","vehicle_makes_u_turn", \
#     "vehicle_moves","vehicle_starts","vehicle_stops"]

# k4_cats = ["person_carries_object","person_closes_facility_or_vehicle_door", \
#             "person_enters_facility_or_vehicle","person_exits_facility_or_vehicle", \
#             "person_opens_facility_or_vehicle_door","vehicle_starts","vehicle_stops"]

# k5_cats = ["person_carries_object","person_closes_facility_or_vehicle_door", \
#     "person_enters_facility_or_vehicle","person_exits_facility_or_vehicle", \
#     "person_opens_facility_or_vehicle_door","person_opens_trunk","person_pickups_object", \
#     "person_pushs_object","person_stands","person_talks_on_phone","person_talks_to_person", \
#     "person_texts_on_phone","vehicle_drops_off_person","vehicle_makes_u_turn", \
#     "vehicle_moves","vehicle_picks_up_person","vehicle_starts","vehicle_stops", \
#     "vehicle_turns_left","vehicle_turns_right"]

# k6_cats = ["person_carries_object","person_closes_facility_or_vehicle_door", \
#     "person_closes_trunk","person_enters_facility_or_vehicle", \
#     "person_exits_facility_or_vehicle","person_opens_trunk","person_stands", \
#     "person_talks_on_phone","person_texts_on_phone", \
#     "vehicle_drops_off_person","vehicle_makes_u_turn","vehicle_moves","vehicle_starts","vehicle_stops"]

# k7_cats = ["person_carries_object","person_pickups_object","person_runs", \
#     "person_talks_on_phone","person_talks_to_person", "person_texts_on_phone", \
#     "vehicle_moves","vehicle_starts","vehicle_stops","vehicle_turns_left", "vehicle_turns_right"]

# k8_cats = ["person_runs","person_talks_on_phone","vehicle_moves"] X3D

# k9_cats = ["person_carries_object","person_closes_trunk","person_exits_facility_or_vehicle"\
#     "person_texts_on_phone","vehicle_starts","vehicle_stops","vehicle_turns_right"] Slowfast

# ["vehicle_makes_u_turn", \
#     "vehicle_moves","vehicle_starts","vehicle_stops", \
#     "vehicle_turns_left","vehicle_turns_right"]

k_cats = ["person_carries_object","person_closes_trunk","person_exits_facility_or_vehicle"\
    "person_texts_on_phone","vehicle_starts","vehicle_stops","vehicle_turns_right"] 
k_path = "/data/kevinq/exps/subk1_l/output_prune_rnd5.json"
l_path = "/data/kevinq/exps/subk1_l/output_prune_rnd1.json"
j_name = "/data/kevinq/exps/subk1_l/output_cob.json"
js_k = json.load(open(k_path,"r"))
js_l = json.load(open(l_path,"r"))
new_dict = {}
new_dict["filesProcessed"] = js_l["filesProcessed"]
new_dict["activities"] = []
for act_k in js_k["activities"]:
    if act_k["activity"] in k_cats:
        new_dict["activities"].append(act_k)
for act_l in js_l["activities"]:
    if act_l["activity"] not in k_cats:
        new_dict["activities"].append(act_l)
json_str = json.dumps(new_dict,indent=4)
with open(j_name, 'w') as save_json:
    save_json.write(json_str)

# k1_cats = ["person_carries_object","vehicle_starts","vehicle_stops","vehicle_turns_right"] 
# k2_cats = ["person_closes_facility_or_vehicle_door", \
#     "person_closes_trunk","person_enters_facility_or_vehicle", \
#     "person_exits_facility_or_vehicle","person_opens_trunk","person_stands", \
#     "person_talks_on_phone","person_texts_on_phone", \
#     "vehicle_drops_off_person","vehicle_makes_u_turn", \
#         "vehicle_moves","vehicle_starts","vehicle_stops"]
        
# k1_path = "/data/kevinq/exps/subk1_l/output_prune_rnd5.json"
# k2_path = "/data/kevinq/exps/subk6/output_mod.json"
# l_path = "/data/kevinq/exps/subk1_l/output_prune_rnd4.json"
# j_name = "/data/kevinq/exps/subk1_l/output_cob.json"
# js_k1 = json.load(open(k1_path,"r"))
# js_k2 = json.load(open(k2_path,"r"))
# js_l = json.load(open(l_path,"r"))
# new_dict = {}
# new_dict["filesProcessed"] = js_l["filesProcessed"]
# new_dict["activities"] = []
# for act_k in js_k1["activities"]:
#     if act_k["activity"] in k1_cats:
#         new_dict["activities"].append(act_k)
# for act_k in js_k2["activities"]:
#     if act_k["activity"] in k2_cats:
#         new_dict["activities"].append(act_k)
# for act_l in js_l["activities"]:
#     if act_l["activity"] not in k1_cats and act_l["activity"] not in k2_cats:
#         new_dict["activities"].append(act_l)
# json_str = json.dumps(new_dict,indent=4)
# with open(j_name, 'w') as save_json:
#     save_json.write(json_str)
