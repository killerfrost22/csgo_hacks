import time
import math
import cv2 as cv
import numpy as np
import win32api
import win32gui
import win32con
import win32ui
from windowUtils import grab_screen

windowHWND = win32gui.FindWindow(None, r'Counter-Strike: Global Offensive')

font = cv.FONT_HERSHEY_SIMPLEX
fontColor = (255, 255, 255)
lineType = 2

colect_data = False
block_width = 640
block_height = 360

fps_avg_list = []
input("Press enter to start data collection...")
collection_start_time = int(time.time())
frame_i = 0
folder_name = "collected_data"
fps = 0
while True:


    start = time.time()

    # Limit FPS
    if fps > 20:
        time.sleep(1/fps)

    # Grab window bitmap
    winRawrect = win32gui.GetWindowRect(windowHWND)
    windowScr = grab_screen(winRawrect)
    h, w, _ = windowScr.shape
    # Image processing
    # cropped = cvim[25:h, 0:w]
    resized = cv.resize(windowScr, (1280, 720), interpolation=cv.INTER_LINEAR)
    # Draw a rectangle around the window's center
    cv.rectangle(resized, (w // 2 - block_width // 2, h // 2 - block_height // 2),
                            (w // 2 + block_width // 2, h // 2 + block_height // 2),
                            (255, 255, 255), 2)

    cropped = resized[h // 2 - block_height // 2:h // 2 + block_height // 2,
                        w // 2 - block_width // 2:w // 2 + block_width // 2]

    if colect_data:
        frame_i += 1
        im_filename = f"{collection_start_time}_{frame_i}.png"
        cv.imwrite(f"{folder_name}/{im_filename}", cropped)


    # Calculate FPS
    end = time.time()
    seconds = end - start

    fps_avg_list.append(seconds)
    if len(fps_avg_list) > 60:
        fps_avg_list.pop(0)

    fps = sum(fps_avg_list) / len(fps_avg_list)
    fps = 1 / fps



    cv.putText(resized, str(round(fps, 2)),
                (0, h - 20),
                font,
                0.5,
                fontColor,
                lineType)

    cv.imshow("OpenCV Window", resized)
    print(f"Collected {frame_i} frames")


    # time.sleep(0.2)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break


cv.destroyAllWindows()