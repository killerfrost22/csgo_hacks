import time
import serial
import math
import cv2 as cv
import numpy as np
import win32api
import win32gui
import win32con
import win32ui
from windowUtils import grab_screen
import colour
# F:\repos\mouse-bot



body_detector = cv.CascadeClassifier("body/cascade.xml")
head_detector = cv.CascadeClassifier("head/cascade.xml")


hwnd = win32gui.FindWindow(None, r'Counter-Strike: Global Offensive')

font = cv.FONT_HERSHEY_SIMPLEX
fontColor = (255, 255, 255)
lineType = 2
aimbot_enabled = True




def rectContains(rect, pt):
    return rect[0] < pt[0] < rect[0] + rect[2] and rect[1] < pt[1] < rect[1] + rect[3]

def rectIntersect(rect1, rect2):
    return rect1[0] < rect2[0] + rect2[2] and rect1[0] + rect1[2] > rect2[0] and rect1[1] < rect2[1] + rect2[3] and rect1[1] + rect1[3] > rect2[1]


if aimbot_enabled:
    def mouse_move(x, y):
        x = int(x).to_bytes(4, byteorder='little', signed=True)
        y = int(y).to_bytes(4, byteorder='little', signed=True)
        ser.write(bytes([ord('<'), *x, *y, ord('>')]))
        return

    def click():
        ser.write(bytes([ord('^')]))

    ser = serial.Serial(
        port='COM8',
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
    )

    assert ser.isOpen()





def draw_all_rects(src, rects):
    for i, (px, py, pw, ph) in enumerate(rects):
        cv.rectangle(src, (px, py), (px + pw, py + ph),
                     (255, 255, 0), 2)


def cascade_real_time_preview():
    fps_avg_list = []
    block_width = 250
    block_height = 250
    last_x2 = False
    avg_color = (0, 0, 0)
    while True:
        start = time.time()

        # Grab window bitmap
        win_rect = win32gui.GetWindowRect(hwnd)
        cvim = grab_screen(win_rect, True)
        # convert to black and white
        h, w, _ = cvim.shape


        # Image processing


        # Gey keyboard state
        state_left = win32api.GetAsyncKeyState(0x01) != 0
        state_right = win32api.GetAsyncKeyState(0x02) != 0
        state_x1 = win32api.GetAsyncKeyState(0x05) != 0
        state_x2 = win32api.GetAsyncKeyState(0x06) != 0

        # Detect faces
        cropped = cvim[(h - block_height) // 2: (h + block_height) // 2,
                            (w - block_width) // 2: (w + block_width) // 2]
        results = body_detector.detectMultiScale3(cropped, scaleFactor=1.1,
                                            minNeighbors=7,
                                            flags=cv.CASCADE_FIND_BIGGEST_OBJECT,
                                            outputRejectLevels = True)
        head_results = head_detector.detectMultiScale(cropped, scaleFactor=1.4,
                                            maxSize=(int(min(block_height*0.8, block_width*0.8)), int(min(block_height*0.8, block_width*0.8))),
                                            minNeighbors=6,
                                            flags=cv.CASCADE_FIND_BIGGEST_OBJECT)

        if state_x2 and last_x2:
            _avg_color = cvim[(h - 5) // 2: (h + 5) // 2,
                            (w - 5) // 2: (w + 5) // 2]

            col1_lab = cv.cvtColor(_avg_color, cv.COLOR_RGB2Lab)
            col2_lab = cv.cvtColor(avg_color, cv.COLOR_RGB2Lab)
            delta_E = colour.delta_E(col1_lab, col2_lab)
            if np.mean(delta_E) > 5:
                click()
                last_x2 = False
        elif state_x2 and not last_x2:
            avg_color = cvim[(h - 5) // 2: (h + 5) // 2,
                            (w - 5) // 2: (w + 5) // 2]

            #last_x2 = True
        # elif not state_x2 and last_x2:
        #     last_x2 = False

        last_x2 = state_x2
        # If avg is different from the current color, click


        # Draw all head rects
        for bx, by, bw, bh in head_results:
            bx += (w - block_width) // 2
            by += (h - block_height) // 2
            cv.rectangle(cvim, (bx, by), (bx + bw, by + bh),
                         (255, 255, 255), 4)

        rects =results[0]
        # neighbours = results[1]
        weights = results[2]
        confidence = [sum(weights[i]) for i in range(len(rects))]

        # Filter all rects whose confidence is less than 1
        rects = [rects[i] for i in range(len(rects)) if confidence[i] > 1]
        confidence = [confidence[i] for i in range(len(confidence)) if confidence[i] > 1]

        # Draw all body rects and their confidence
        for i, (bx, by, bw, bh) in enumerate(rects):
            bx += (w - block_width) // 2
            by += (h - block_height) // 2
            cv.rectangle(cvim, (bx, by), (bx + bw, by + bh),
                         (255, 0, 0), 2)
            cv.putText(cvim, str(round(confidence[i],2)),
                       (bx, by - 10), font, 0.5, fontColor, lineType)


        if len(rects) > 0:
            # Get the closest rectangle from the center of the cropped image
            min_dist = -1
            closest_index = -1
            for i, rect in enumerate(rects):
                rect_center = ((rect[0] + rect[2] // 2), (rect[1] + rect[3] // 2))
                dist = math.sqrt((rect_center[0] - block_width // 2)**2 + (rect_center[1] - block_height // 2)**2)
                if min_dist == -1 or dist < min_dist:
                    min_dist = dist
                    closest_index = i






            # Draw a rectangle on the closest rectangle
            bx, by, bw, bh = rects[closest_index]
            bx += (w - block_width) // 2
            by += (h - block_height) // 2
            cv.rectangle(cvim, (bx, by), (bx + bw, by + bh),
                            (255, 0, 255), 2)

            head_rect = None
            if len(head_results) > 0:
                # Find the uppermost head

                for hx, hy, hw, hh in head_results:
                    hx += (w - block_width) // 2
                    hy += (h - block_height) // 2
                    intersects = rectIntersect((bx, by, bw, bh), (hx, hy, hw, hh))
                    if intersects and (
                        head_rect is not None
                        and hy < head_rect[1]
                        or head_rect is None
                    ):
                        head_rect = (hx, hy, hw, hh)


                if head_rect is not None:
                    # Check if head height is greater than 50% of body height
                    # and head width greater than 110% of body width
                    if head_rect[3] > bh * 0.5 or ( # Head height is greater than 50% of body height
                            head_rect[2] > bw * 1.1) or ( # Head width is greater than 110% of body width
                            # Head is not too far from y-axis of body
                            abs(head_rect[1] - by) > bh * 0.5
                        ):
                        head_rect = None
                    else:
                        # Draw head rect
                        hx, hy, hw, hh = head_rect
                        cv.rectangle(cvim, (hx, hy), (hx + hw, hy + hh),
                                    (0, 255, 0), 4)




            # Draw a line from the center of cropped to the center of the rectangle (or head)
            cv.line(cvim, (w//2 , h//2), (bx + bw // 2, by + bh // 2), (0, 255, 255), 2)

            if aimbot_enabled:
                # Get the delta from the center of the screen to the center of the rectangle (or head)
                if head_rect is not None:
                    hx, hy, hw, hh = head_rect
                    x_delta =  (hx + hw // 2) - (w // 2)
                    y_delta  = (hy + int(hh * 0.1)) - (h // 2)
                else:
                    # Move the ry +20% of the height of the rectangle (to approximate the head)
                    x_delta = (bx + bw // 2) - (w // 2)
                    y_delta = (by + int(bh * 0.2)) - (h // 2) if by > h // 2 else 0
                                    # x_delta *= 0.01 # May be false positive so we reduce the delta
                                    # y_delta *= 0.01


                #if x_delta != 0 and abs(x_delta) > bw:
                x_delta *= 1

                #if y_delta != 0 and abs(y_delta) > bw:
                y_delta = 0

                if  state_x1:
                    x_delta = math.ceil(x_delta)
                    y_delta = math.ceil(y_delta)
                    mouse_move(x_delta, y_delta)



        cv.rectangle(cvim, (w // 2 - block_width // 2,h // 2 - block_height // 2),
                            (w // 2 + block_width // 2, h // 2 + block_height // 2),
                            (255, 255, 255), 2)

        # Calculate FPS
        end = time.time()
        seconds = end - start
        fps_avg_list.append(seconds)
        if len(fps_avg_list) > 60:
            fps_avg_list.pop(0)

        fps = sum(fps_avg_list) / len(fps_avg_list)
        fps = 1 / fps
        cv.putText(cvim, str(round(fps, 2)),
                   (0, h - 32),
                   font,
                   0.5,
                   fontColor,
                   lineType)
        # Resize the image to 1280x720
        resized = cv.resize(cvim, (1280, 720))
        cv.imshow("Frame", resized)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break


cascade_real_time_preview()
# data_collection_loop()
#
#
# cap.release()

cv.destroyAllWindows()
