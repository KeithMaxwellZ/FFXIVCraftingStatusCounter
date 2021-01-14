import os
import json

from util import COLOR_DICT

f_list = os.listdir("data")
res = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0}
for i in f_list:
    if os.path.splitext(i)[1] == ".txt":
        with open(f"data/{i}", "r") as f:
            tmp = json.load(f)
            for x in range(1, 11):
                res[f"{x}"] += tmp[f"{x}"]

total = 0
for i in range(1, 10):
    total += res[str(i)]

s = ""
for i in range(1, 10):
    s += f"{COLOR_DICT[i]}:{res[str(i)]} ------ {format(res[str(i)]/total, '.2f')}" + "\n"
    print(s)

with open("res.txt", 'w', encoding='utf-8') as f:
    f.write(s)