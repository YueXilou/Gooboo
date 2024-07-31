import copy
import cv2
import numpy as np
import pyautogui as gui
import time
import script_tools as tools
import math


def calculator(cal_type, num_a, num_b):
    if cal_type == 1:
        return num_a+num_b
    elif cal_type == 2:
        return num_a-num_b
    elif cal_type == 3:
        return num_a*num_b
    elif cal_type == 4:
        return num_a/num_b
    elif cal_type == 5:
        return math.sqrt(num_b)
    elif cal_type == 6:
        return pow(num_a, num_b)


# initialization procedure
empty_pack = tools.PicturePack(0)
op_pack = tools.PicturePack(17)
state_pack = tools.PicturePack(2)
for i in range(17):
    op_pack.load_picture(cv2.imread('./data/num'+str(i)+'.jpg'))
for i in range(2):
    state_pack.load_picture(cv2.imread('./data/state_'+str(i)+'.jpg'))
input_area = tools.Area(op_pack, [50, 215], 1850, 55, 0.7)
state_area = tools.Area(state_pack, [35, 157], 1443, 389, 0.8)

time.sleep(2)

# k-range can be changed.
for k in range(1000000):

    time.sleep(0.08)

    temp = tools.screenshot()

    state, _, state_place = state_area.match(temp, type=1)
    if state == 1:
        temp_gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
        ret, temp_bi = cv2.threshold(temp_gray, 200, 255, cv2.THRESH_BINARY)
        # cv2.imshow('',input_area.cut(temp))
        # cv2.waitKey(0)
        # cv2.imshow('',input_area.cut(temp_bi))
        # cv2.waitKey(0)
        project = np.zeros(input_area.width)
        for i in range(input_area.width):
            for j in range(input_area.height):
                project[i] += input_area.cut(temp_bi)[j][i]
        flag = 0
        cut_result = []
        cut_temp = [0, 0]
        for i in range(input_area.width):
            if flag == 0:
                if project[i] > 0:
                    cut_temp[flag] = i - 6
                    flag = 1 - flag
            elif flag == 1:
                if project[i] == 0:
                    cut_temp[flag] = i + 6
                    flag = 1 - flag
                    cut_result.append(copy.deepcopy(cut_temp))

        print(cut_result)
        left_num = ''
        right_num = ''
        op = 0
        flag = 0
        for i in range(len(cut_result)):
            pict_temp = input_area.cut(temp)[:, cut_result[i][0]: cut_result[i][1]]
            # cv2.imshow('',pict_temp)
            # cv2.waitKey(0)
            if cut_result[i][1] - cut_result[i][0] > 18:
                match_result = input_area.match(pict_temp, type=1)[0]
                if match_result < 10:
                    if op == 0:
                        left_num += str(match_result)
                    else:
                        right_num += str(match_result)
                else:
                    if match_result < 16 and flag == 0:
                        op = match_result-9
                        if left_num == '':
                            left_num = '0'
                    elif match_result == 16:
                        flag = 1
                        if op == 0:
                            left_num += 'e'
                        else:
                            right_num += 'e'
                    elif flag == 1:
                        if op == 0:
                            if match_result == 10:
                                left_num += '+'
                            else:
                                left_num += '-'
                        else:
                            if match_result == 10:
                                right_num += '+'
                            else:
                                right_num += '-'
                        flag = 0
            else:
                if op == 0:
                    left_num += '.'
                else:
                    right_num += '.'
        left_num = int(float(left_num))
        right_num = int(float(right_num))
        result = str(int(calculator(op, left_num, right_num)))

        print(left_num,right_num,result)

        gui.PAUSE = 0.0005
        for i in range(len(result)):
            gui.press(result[i])
        gui.press('enter')

    elif state == 0:
        gui.click(state_place[0], state_place[1] + 125)
        time.sleep(1)
