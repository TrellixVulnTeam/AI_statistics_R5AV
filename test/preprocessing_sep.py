# #-*- coding: utf-8 -*-
import os
import shutil

path = "./match_test/" # os.walk 경로
delete_folder_path = "./match_test/delete/" # 삭제 파일 경로

for root, dirs, files in os.walk(path):
    for file_name in files:
        print(file_name)
        match_flag = False

        if file_name.split(".")[1].lower() == "jpg":
            for root_j, dirs_j, files_j in os.walk(path):
                for file_name_j in files_j:
                    if file_name_j == file_name.split(".")[0] + ".json":
                        match_flag = True
                    if file_name.split(".")[0][-1] == "P":
                        if file_name_j == file_name.split(".")[0][:-1] + "0.json":
                            shutil.move(root_j + "/" + file_name_j, delete_folder_path + file_name_j)
                            if file_name_j in files:
                                files.remove(file_name_j)
                        if file_name_j == file_name.split(".")[0][:-1] + "0.jpg":
                            shutil.move(root_j + "/" + file_name_j, delete_folder_path + file_name_j)
                            if file_name_j in files:
                                files.remove(file_name_j)

            if not match_flag:
                shutil.move(root + "/" + file_name, delete_folder_path + file_name)
                if file_name in files:
                    files.remove(file_name)

        elif file_name.split(".")[1].lower() == "json":
            for root_j, dirs_j, files_j in os.walk(path):
                for file_name_j in files_j:
                    if file_name_j == file_name.split(".")[0] + ".jpg":
                        match_flag = True
                    if file_name.split(".")[0][-1] == "P":
                        if file_name_j == file_name.split(".")[0][:-1] + "0.json":
                            shutil.move(root_j + "/" + file_name_j, delete_folder_path + file_name_j)
                            if file_name_j in files:
                                files.remove(file_name_j)
                        if file_name_j == file_name.split(".")[0][:-1] + "0.jpg":
                            shutil.move(root_j + "/" + file_name_j, delete_folder_path + file_name_j)
                            if file_name_j in files:
                                files.remove(file_name_j)

            if not match_flag:
                shutil.move(root + "/" + file_name, delete_folder_path + file_name)
                if file_name in files:
                    files.remove(file_name)