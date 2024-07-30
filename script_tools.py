import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui as gui
import time


def screenshot(region=(0, 0, 1920, 1080)):
    """
    :param region: start_x, start_y, length, height
    :return: BGR in cv2
    """
    screen_temp = ImageGrab.grab(bbox=region)
    screen_temp = cv2.cvtColor(np.array(screen_temp), cv2.COLOR_RGB2BGR)
    return screen_temp


def rgb2bgr(input_picture):
    return cv2.cvtColor(input_picture, cv2.COLOR_RGB2BGR)


def bgr2rgb(input_picture):
    return cv2.cvtColor(input_picture, cv2.COLOR_BGR2RGB)


def bgr2hsv(input_picture):
    return cv2.cvtColor(input_picture, cv2.COLOR_BGR2HSV)


def template_match(input_picture, template, template_num, template_threshold):
    max_num = -1
    max_temp = 0
    loc_temp = [0, 0]
    for match_num in range(template_num):
        template_result = cv2.matchTemplate(input_picture, template[match_num], cv2.TM_CCOEFF_NORMED)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(template_result)
        if maxVal > max_temp:
            max_temp = maxVal
            max_num = match_num
            loc_temp = maxLoc
    if max_temp < template_threshold:
        max_num = -1
    return max_num, max_temp, loc_temp


class PicturePack:

    def __init__(self, picture_num):
        self.total_num = picture_num
        self.pic = []

    def load_picture(self, picture):
        self.pic.append(picture)

    def __add__(self, to_add):
        result = PicturePack(self.total_num + to_add.total_num)
        result.pic = self.pic + to_add.pic
        return result


class Area:

    def __init__(self, picture_pack, place, width, height, match_threshold):
        self.pack = picture_pack
        self.coordinate = place
        self.width = width
        self.height = height
        self.threshold = match_threshold
        self.sub_area = {}
        self.flag = -1

    def __getitem__(self, item):
        return self.sub_area[item]

    def cut(self, pict):
        return pict[
               self.coordinate[1]:self.coordinate[1] + self.height,
               self.coordinate[0]:self.coordinate[0] + self.width
               ]

    def add_sub(self, sub_area, area_name):
        self.sub_area[area_name] = sub_area
        return True

    def match(self, pict, type = 0):
        """
        :param pict:
        :return:
        """
        if type == 0:
            pict = self.cut(pict)
        match_result = template_match(pict, self.pack.pic, self.pack.total_num, self.threshold)
        self.flag = match_result[0]
        return match_result

    def move(self):
        gui.moveTo(self.coordinate[0] + 0.5 * self.width, self.coordinate[1] + 0.5 * self.height)
        return True

    def click(self):
        self.move()
        gui.mouseDown()
        time.sleep(0.05)
        gui.mouseUp()
        return True


if __name__ == '__main__':
    temp = screenshot()
    cv2.imshow('', temp)
    cv2.waitKey(0)
    pack = PicturePack(1)
    pack.load_picture(temp)
    area = Area(pack, [0, 0], 192, 108, 0.4)
    area.add_sub(area, 'temp')
    temp_1 = area.cut(temp)
    cv2.imshow('', area['temp'].cut(temp))
    cv2.waitKey(0)
    print(area.match(temp_1))
    print(area['temp'])
