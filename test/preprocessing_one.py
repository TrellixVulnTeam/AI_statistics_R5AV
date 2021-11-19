# # #-*- coding: utf-8 -*-
import os
import shutil

path = "./match_test/" # os.walk 경로
delete_folder_path = "./delete/" # 삭제 파일 경로

for root, dirs, files in os.walk(path):
    for file_name in files:
        print(file_name)
        if file_name.split(".")[-1].lower() == "jpg":
            if file_name.split(".")[0][-1] == "P":
                if os.path.exists(root + "/" + file_name.split(".")[0][:-1] + "0.json"):
                    shutil.move(root + "/" + file_name.split(".")[0][:-1] + "0.json", delete_folder_path + file_name.split(".")[0][:-1] + "0.json")
                    if file_name.split(".")[0][:-1] + "0.json" in files:
                        files.remove(file_name.split(".")[0][:-1] + "0.json")
                if os.path.exists(root + "/" + file_name.split(".")[0][:-1] + "0.jpg"):
                    shutil.move(root + "/" + file_name.split(".")[0][:-1] + "0.jpg", delete_folder_path + file_name.split(".")[0][:-1] + "P.jpg")
                    if file_name.split(".")[0][:-1] + "0.jpg" in files:
                        files.remove(file_name.split(".")[0][:-1] + "0.jpg")

            if os.path.exists(root + "/" + file_name.split(".")[0] + ".json"):
                continue
            else:
                shutil.move(root + "/" + file_name, delete_folder_path + file_name)

        if file_name.split(".")[-1].lower() == "json":
            if file_name.split(".")[0][-1] == "P":
                if os.path.exists(root + "/" + file_name.split(".")[0][:-1] + "0.json"):
                    shutil.move(root + "/" + file_name.split(".")[0][:-1] + "0.json", delete_folder_path + file_name.split(".")[0][:-1] + "0.json")
                    if file_name.split(".")[0][:-1] + "0.json" in files:
                        files.remove(file_name.split(".")[0][:-1] + "0.json")
                if os.path.exists(root + "/" + file_name.split(".")[0][:-1] + "0.jpg"):
                    shutil.move(root + "/" + file_name.split(".")[0][:-1] + "0.jpg", delete_folder_path + file_name.split(".")[0][:-1] + "0.jpg")
                    if file_name.split(".")[0][:-1] + "0.jpg" in files:
                        files.remove(file_name.split(".")[0][:-1] + "0.jpg")

            if os.path.exists(root + "/" + file_name.split(".")[0] + ".jpg"):
                continue
            else:
                shutil.move(root + "/" + file_name, delete_folder_path + file_name)

