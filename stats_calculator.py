import os
import json

f_list = os.listdir("data")
res = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0}
for i in f_list:
    if os.path.splitext(i)[1] == ".txt":
        with open(f"data/{i}", "r") as f:
            tmp = json.load(f)
            for x in range(1, 11):
                res[f"{x}"] += tmp[f"{x}"]

print(res)
