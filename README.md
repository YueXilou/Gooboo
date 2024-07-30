# Gooboo
 A script for game Gooboo

## Environment
 It is tested on Python 3.11\(maybe it still works on earlier version\)  
 To successfully compile it you need:
 1. cv2
 2. numpy
 3. pyautogui
 4. PIL

## How to use
 You should first download all the files in this repo except the 'Source' folder. Then open and run cal.py, it will work after 2 seconds so keep your gooboo game's school interface on the very top and wait. it will automatically start learn, answer math question and learn again and again. You can stop it by moving your cursor to the left-above corner of the screen since it will send a error to pyautogui module LOL.

## Script's procedure
 It starts by capturing your screen, judging which state you are. When it finds you need to answer the math question, it will then try to recognize the question and calculate the answer, then it inputs the answer by pyautogui module.
