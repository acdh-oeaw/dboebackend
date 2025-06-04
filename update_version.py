import sys
import json


data = None
with open("version.json", "r") as jsonFile:
    data = json.load(jsonFile)
    data["version"]["sw"] = sys.argv[1]

with open("version.json", "w") as jsonFile:
    json.dump(data, jsonFile)
