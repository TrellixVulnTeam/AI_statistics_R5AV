#-*- coding: utf-8 -*-
import os
import copy
import openpyxl

def main():
    ############ 변수 ############
    filtering_folder = ["delete","video","dldelete","dcteam00","save"]

    dc_rank_day_list = []
    day_list = []
    dc_rank_day_dict_form = {
    "id": "",
    "day": "",
    "checked_image_count": 0,
    "json_count": 0
    }
    ###########################################      통계 데이터 작성      #########################################################
    for root, dirs, files in os.walk("../"):
        # DC 폴더 필터링
        dirs[:] = [dir for dir in dirs if dir.lower() not in filtering_folder]

        if len(files) > 0:
            for file_name in files:
                print("File : " + root + "/" + file_name)
                check_in_list_flag = False
                idx = 0

                if file_name[0] == "G":
                    id = "000002"
                    day = "0000-00-00"
                elif file_name.split(".")[-1] in ["jpg","json"]:
                    id = file_name.split("_")[0]
                    day = file_name.split("_")[1].split(" ")[0]
                else:
                    continue

                day_list.append(day)

                for i, dc_rank_day in enumerate(dc_rank_day_list):
                    if dc_rank_day["id"] == id and dc_rank_day["day"] == day:
                        idx = i
                        check_in_list_flag = True
                        break

                if check_in_list_flag:
                    if file_name.split(".")[-1] == "jpg":
                        dc_rank_day_list[idx]["checked_image_count"] += 1
                    elif file_name.split(".")[-1] == "json":
                        if file_name.split(".")[0][-1].lower() == "s":
                            dc_rank_day_list[idx]["json_count"] += 1
                else:
                    dc_rank_day_dict = copy.deepcopy(dc_rank_day_dict_form)
                    dc_rank_day_dict["id"] = id
                    dc_rank_day_dict["day"] = day
                    if file_name.split(".")[-1] == "jpg":
                        dc_rank_day_dict["checked_image_count"] += 1
                    elif file_name.split(".")[-1] == "json":
                        if file_name.split(".")[0][-1].lower() == "s":
                            dc_rank_day_dict["json_count"] += 1
                    dc_rank_day_list.append(dc_rank_day_dict)

    ###########################################      엑셀 그리기      #########################################################
    dc_wb = openpyxl.load_workbook('DC_Personal_Form.xlsx')

    ###########################################      ID-날짜 시트      #########################################################
    day_list = list(set(day_list))
    day_list.sort()

    dc_personal_sheet = dc_wb.copy_worksheet(dc_wb['DC_Form'])

    idx = 7

    for i, dc_rank_day in enumerate(dc_rank_day_list):
        dc_personal_sheet['A' + str(i + idx)] = i

        id = dc_rank_day["id"]
        dc_personal_sheet['B' + str(i + idx)] = dc_rank_day["day"]
        dc_personal_sheet['C' + str(i + idx)] = dc_personal_sheet['G5'].value
        dc_personal_sheet['D' + str(i + idx)] = dc_rank_day["checked_image_count"]
        dc_personal_sheet['E' + str(i + idx)] = dc_rank_day["json_count"]
        dc_personal_sheet['F' + str(i + idx)] = dc_rank_day["checked_image_count"] - dc_personal_sheet['G5'].value

    dc_personal_sheet.title = id + "-수집현황"
    dc_personal_sheet['A1'] = id + " 수집현황"
    dc_personal_sheet['A2'] = day_list[0] + " ~ " + day_list[-1]

    dc_wb.remove(dc_wb['DC_Form'])
    if not (os.path.isdir("./output")):
        os.makedirs(os.path.join("./output"))
    dc_wb.save('./output/DC_Personal.xlsx')

try:
    main()
except Exception as e:
    print(e)
    while(True):
        continue