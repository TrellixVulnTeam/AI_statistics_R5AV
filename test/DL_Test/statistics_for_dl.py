#-*- coding: utf-8 -*-
import json
import os
import copy
import openpyxl

def main():
    ############ 변수 ############
    filtering_folder = ["delete","video","dldelete","dcteam00","save"]

    dl_id_day_list = []
    dl_id_total_list = []
    day_list = []
    dl_id_day_dict_form = {
    "id":"",
    "day":"",
    "flatness_A":0,
    "flatness_B":0,
    "flatness_C":0,
    "flatness_D":0,
    "flatness_E":0,
    "walkway_paved":0,
    "walkway_block":0,
    "paved_state_broken":0,
    "paved_state_normal":0,
    "block_state_broken":0,
    "block_state_normal":0,
    "block_kind_bad":0,
    "block_kind_good":0,
    "outcurb_rectangle":0,
    "outcurb_slide":0,
    "outcurb_rectangle_broken":0,
    "outcurb_slide_broken":0,
    "restspace":0,
    "sidegap_in" :0,
    "sidegap_out" :0,
    "sewer_cross" :0,
    "sewer_line" :0,
    "brailleblock_dot":0,
    "brailleblock_line":0,
    "brailleblock_dot_broken":0,
    "brailleblock_line_broken" :0,
    "continuity_tree":0,
    "continuity_manhole":0,
    "ramp_yes":0,
    "ramp_no":0,
    "bicycleroad_broken":0,
    "bicycleroad_normal":0,
    "planecrosswalk_broken":0,
    "planecrosswalk_normal" :0,
    "steepramp":0,
    "bump_slow":0,
    "bump_zigzag":0,
    "weed":0,
    "floor_normal":0,
    "floor_broken":0,
    "flowerbed":0,
    "parkspace":0,
    "tierbump":0,
    "stone":0,
    "enterrail":0,
    "fireshutter":0,

    "stair_normal":0,
    "stair_broken":0,
    "wall":0,
    "window_sliding":0,
    "window_casement":0,
    "pillar":0,
    "lift":0,
    "door_normal":0,
    "door_rotation":0,
    "lift_door":0,
    "resting_place_roof":0,
    "reception_desk":0,
    "protect_wall_protective":0,
    "protect_wall_guardrail":0,
    "protect_wall_kickplate":0,
    "handle_vertical":0,
    "handle_lever":0,
    "handle_circular":0,
    "lift_button_normal":0,
    "lift_button_openarea":0,
    "lift_button_layer":0,
    "lift_button_emergency":0,
    "direction_sign_left":0,
    "direction_sign_right":0,
    "direction_sign_straight":0,
    "direction_sign_exit":0,
    "sign_disabled_toilet":0,
    "sign_disabled_parking":0,
    "sign_disabled_elevator":0,
    "sign_disabled_ramp":0,
    "sign_disabled_callbell":0,
    "sign_disabled_icon":0,
    "braille_sign":0,
    "chair_multi":0,
    "chair_one":0,
    "chair_circular":0,
    "chair_back":0,
    "chair_handle":0,
    "number_ticket_machine":0,
    "beverage_vending_machine":0,
    "beverage_desk":0,
    "trash_can":0,
    "mailbox":0
    }

    ###########################################      통계 데이터 작성      #########################################################
    for root, dirs, files in os.walk("../Labelme_test"):
        # DL 폴더 필터링
        dirs[:] = [dir for dir in dirs if dir.lower() not in filtering_folder and dir[:2] != "DC"]

        if len(files) > 0:
            for file_name in files:
                check_in_list_flag = False
                idx = 0

                if file_name.split(".")[-1] == "json":
                    if file_name.split(".")[0][-1].lower() == "s":
                        continue
                    print("File : " + root + "/" + file_name)

                    dl_id = root.split("\\")[-2].split("_")[0]
                    dl_day = root.split("\\")[-2].split("_")[1]

                    day_list.append(dl_day)

                    for i, dl_id_day in enumerate(dl_id_day_list):
                        if dl_id_day["id"] == dl_id and dl_id_day["day"] == dl_day:
                            idx = i
                            check_in_list_flag = True
                            break

                    json_file = open(root + "\\" + file_name,"rt",encoding="UTF8")
                    jsonString = json.load(json_file)

                    if jsonString.get("annotations") != None:
                        category_id = jsonString.get("annotations")
                        category_key = "category_id"
                    else:
                        category_id = jsonString.get("shapes")
                        category_key = "label"

                    for shapes in category_id:
                        if check_in_list_flag:
                            dl_id_day_list[idx][shapes[category_key]] += 1
                        else:
                            dl_id_day_dict = copy.deepcopy(dl_id_day_dict_form)
                            dl_id_day_dict["id"] = dl_id
                            dl_id_day_dict["day"] = dl_day
                            dl_id_day_dict[shapes[category_key]] += 1
                            dl_id_day_list.append(dl_id_day_dict)
                            idx = len(dl_id_day_list) - 1
                            check_in_list_flag = True

    ###########################################      엑셀 그리기      #########################################################
    day_list=list(set(day_list))
    day_list.sort()

    for day_idx in range(1, len(day_list) + 1):
        dl_wb = openpyxl.load_workbook('DL_Personal_Form.xlsx')
        statistics_day_list = day_list[0:day_idx]

        ###########################################      ID-날짜 시트      #########################################################
        for dl_id_day in dl_id_day_list:
            if dl_id_day["day"] != statistics_day_list[-1]:
                continue
            dl_id_day_sheet = dl_wb.copy_worksheet(dl_wb['Id_Day_Form'])
            idx = 4

            for key, value in dl_id_day.items():
                if key == "id":
                    id = value
                    continue
                elif key == "day":
                    day = value
                    continue
                if idx == 50:
                    idx = 53
                dl_id_day_sheet['J' + str(idx)] = value
                idx += 1

            dl_id_day_sheet.title = id + "-" + statistics_day_list[-1]
            dl_id_day_sheet['A1'] = id + "-" + statistics_day_list[-1]

        ###########################################      ID-누계 시트      #########################################################
        dl_id_total_list = []
        for dl_id_day in dl_id_day_list:
            if dl_id_day["day"] not in statistics_day_list:
                continue
            check_in_list_flag = False
            idx = 0

            id = dl_id_day["id"]

            for i, dl_id_total in enumerate(dl_id_total_list):
                if dl_id_total["id"] == id:
                    idx = i
                    check_in_list_flag = True
                    break

            for key, value in dl_id_day.items():
                if check_in_list_flag:
                    if key == "id" or key == "day":
                        continue
                    dl_id_total_list[idx][key] += value
                else:
                    dl_id_total_dict = copy.deepcopy(dl_id_day_dict_form)
                    dl_id_total_dict["id"] = id
                    dl_id_total_list.append(dl_id_total_dict)
                    idx = len(dl_id_total_list) - 1
                    check_in_list_flag = True

        for dl_id_total in dl_id_total_list:
            dl_id_total_sheet = dl_wb.copy_worksheet(dl_wb['Id_Total_Form'])
            idx = 5

            for key, value in dl_id_total.items():
                if key == "id":
                    id = value
                    continue
                elif key == "day":
                    continue
                if idx == 51:
                    idx = 54
                dl_id_total_sheet['J' + str(idx)] = value
                idx += 1

            dl_id_total_sheet.title = id + "-누계"
            dl_id_total_sheet['A1'] = id + " - 누계"
            dl_id_total_sheet['A2'] = statistics_day_list[0] + " ~ " + statistics_day_list[-1]

        dl_form_sheet_list = ['Id_Total_Form', 'Id_Day_Form']
        for dl_form_sheet in dl_form_sheet_list:
            dl_wb.remove(dl_wb[dl_form_sheet])
        if not (os.path.isdir("./output")):
            os.makedirs(os.path.join("./output"))
        dl_wb.save('./output/DL_Personal' + statistics_day_list[-1] + '.xlsx')

try:
    main()
except Exception as e:
    print(e)
    while(True):
        continue