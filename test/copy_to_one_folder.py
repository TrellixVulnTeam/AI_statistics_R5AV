#-*- coding: utf-8 -*-
import os
import shutil

nas_folder = ""
one_folder = ""
_s_folder = ""
filtering_folder = ["delete","video","dldelete","dcteam00","save"]

def copy_to_one_folder():
    for root, dirs, files in os.walk(nas_folder):
        dirs[:] = [dir for dir in dirs if dir.lower() not in filtering_folder and dir[:2] != "DC"]

        for file_name in files:
            print(file_name)
            ext = os.path.splitext(file_name)[1]

            if ext.lower() == ".json" and file_name.split(".")[0][-1].lower() == "s":
                shutil.copy(root + "/" + file_name, _s_folder + file_name)
            elif ext.lower() == ".json" or ext.lower() == ".jpg":
                shutil.copy(root + "/" + file_name, one_folder + file_name)

copy_to_one_folder()