#-*- coding: utf-8 -*-
import os
import shutil
import random

test_img_path = "/home/di-01/Downloads/yolov5_data/images/test/"
test_label_path = "/home/di-01/Downloads/yolov5_data/labels/test/"

img_save_path = "/home/di-01/Downloads/yolov5_data/images/"
label_save_path = "/home/di-01/Downloads/yolov5_data/labels/"

folder_num = 0
shuffled_files = []

for root, dirs, files in os.walk(test_img_path):
    shuffled_files = random.shuffle(files)

for i, file in enumerate(shuffled_files):
    if i % 5000 == 0:
        i += 1
    shutil.copy(test_img_path + file, img_save_path + "test" + folder_num + "/" + file)
    shutil.copy(test_label_path + file.split(".")[0] + ".txt", label_save_path + "test" + folder_num + "/" + file.split(".")[0] + ".txt")