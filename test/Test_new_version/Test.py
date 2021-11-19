import json
import os
import copy
import openpyxl

file_list = ["DC0101_2020-10-09 112709_00.json", "DC0101_2020-10-10 092951_DP.json"]

for file in file_list:
    json_file = open(file,"rt",encoding="UTF8")
    jsonString = json.load(json_file)


