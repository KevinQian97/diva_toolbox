import numpy as np
import os
import pandas as pd

f = pd.read_csv("/home/kevinq/repos/diva_toolbox/scorer/scores_by_activity.csv")
act_list = ['hand_interacts_with_person', 'person_abandons_package', 'person_carries_heavy_object', 'person_closes_facility_door', 'person_closes_trunk', 'person_closes_vehicle_door', 'person_embraces_person', 'person_enters_scene_through_structure', 'person_exits_scene_through_structure', 'person_exits_vehicle', 'person_enters_vehicle', 'person_interacts_with_laptop', 'person_loads_vehicle', 'person_opens_facility_door', 'person_opens_trunk', 'person_opens_vehicle_door', 'person_picks_up_object', 'person_purchases', 'person_puts_down_object', 'person_reads_document', 'person_rides_bicycle', 'person_sits_down', 'person_steals_object', 'person_stands_up', 'person_talks_on_phone', 'person_talks_to_person', 'person_texts_on_phone', 'person_transfers_object', 'person_unloads_vehicle', 'vehicle_drops_off_person', 'vehicle_picks_up_person', 'vehicle_makes_u_turn', 'vehicle_reverses', 'vehicle_starts', 'vehicle_stops', 'vehicle_turns_left',"vehicle_turns_right"]

acts = list(f["activity"])
print(acts[0])
print(38%37)
for i in range(len(acts)):
    if acts[i] != act_list[i%37]:
        print(i)