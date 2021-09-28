import json
import os

js_count = json.load(open("./count.json")
)
overlap_thresh = 100
thresh_dict = {}
for k,v in js_count.items():
    if k not in thresh_dict:
        thresh_dict[k] = 0
    threshs = list(v.keys())
    for thresh in threshs:
        if js_count[k][thresh]["overlap"]>overlap_thresh and int(thresh)>thresh_dict[k]:
            thresh_dict[k] = int(thresh)

json_str = json.dumps(thresh_dict,indent=4)
with open("./thresh.json", 'w') as save_json:
    save_json.write(json_str)


