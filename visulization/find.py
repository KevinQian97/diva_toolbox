import json

path = "./output_vis.json"
db = json.load(open(path,"r"))["activities"]
print(len(db))
for act in db:
    if "2018-03-11.11-45-00.11-50-00.school.G330.avi" in act["localization"]:
        if "5632" in act["localization"]["2018-03-11.11-45-00.11-50-00.school.G330.avi"] and act["localization"]["2018-03-11.11-45-00.11-50-00.school.G330.avi"]["5632"]==1:
            if 1747 in act["localization"]["2018-03-11.11-45-00.11-50-00.school.G330.avi"]["bbox"]:
                print(act)