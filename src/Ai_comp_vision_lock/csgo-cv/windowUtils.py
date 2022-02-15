import win32api
import win32gui
import win32con
import win32ui
import numpy as np


def grab_screen(region=None, fs=False):
    desktopHandle = win32gui.GetDesktopWindow()
    desktopDC = win32gui.GetWindowDC(desktopHandle)
    srcDC = win32ui.CreateDCFromHandle(desktopDC)
    memDC = srcDC.CreateCompatibleDC()
    bitmap = win32ui.CreateBitmap()

    if region:
        left, top, x2, y2 = region
        width = x2 - left
        height = y2 - top
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    bitmap.CreateCompatibleBitmap(srcDC, width, height)
    memDC.SelectObject(bitmap)
    memDC.BitBlt((0, 0), (width, height), srcDC, (left, top), win32con.SRCCOPY)

    image_array = bitmap.GetBitmapBits(True)
    img = np.frombuffer(image_array, dtype='uint8')
    img.shape = (height, width, 4)

    srcDC.DeleteDC()
    memDC.DeleteDC()
    win32gui.ReleaseDC(desktopHandle, desktopDC)
    win32gui.DeleteObject(bitmap.GetHandle())

    # Remove windows frame
    h, w, _ = img.shape
    if not fs:
        return img[25:h, 0:w]
    return img
