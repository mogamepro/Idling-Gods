import pyautogui as py
import datetime
import winsound
import win32com
import pytesseract
import win32api
import win32con
import win32gui
import re
import sys
import time
import importlib
from mss import mss, ScreenShotError
from win32com import client
from threading import Timer
from time import sleep
from PIL import ImageGrab
from PIL import Image

def clicky(*coords):
    movey(*coords, 0.1)
    py.click(*coords)

def movey(x, y, duration = 0.1):
    py.moveTo(x, y, duration)

def keyPress(key):
    key = str(key)
    if py.isValidKey(key):
        py.press(key)
    else:
        py.typewrite(key)

def hotkeyPress(*keys):
    py.hotkey(*keys)

def parseNum(num):
    try:
        retNum = float(re.sub(r"[^0-9.]", "", num))
        mult = {'million': 1e6, 'billion': 1e9, 'trillion': 1e12, '.': 1e3}
        if num.count('.') > 1:
            retNum *= 1e3 ** num.count('.')
        else:
            try:
                retNum = [retNum * mult[m] for m in mult if m in num][0]
            except:
                pass
        retNum = int(retNum)
    except ValueError:
        print("Invalid value:", num)
        raise ValueError
    return retNum

def takeAndReadImage(left, top, right, bottom):
    return readImage(takeImage(left, top, right, bottom))

def takeImage(left = 0, top = 0, right = 1980, bottom = 1080):
    try:
        with mss() as sct:
            sct_img = sct.grab((left, top, right, bottom))
            return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
    except ScreenShotError:
        print('mss failed. If this message repeats a lot, then ImageGrab still works (at least for awhile')
        return ImageGrab.grab(bbox=(left, top, right, bottom))

def readImage(im):
    text = pytesseract.image_to_string(im, config = '--psm 7')
    return text

def formatNumber(num):
    return "{:,}".format(num)

def detectKeypress():
    if win32api.GetAsyncKeyState(win32con.VK_CONTROL):
        sys.exit()
    elif win32api.GetAsyncKeyState(win32con.VK_SHIFT):
        return True
    elif win32api.GetAsyncKeyState(win32con.VK_MENU):
        input("Press enter to continue\r")
    return False

def findWindowHandle(title = 'Idle Gods Controller X'):
    hwnd = []
    titles = []
    win32gui.EnumWindows(enumHandler, (hwnd, titles, title))
    if len(hwnd) < 1:
        for val in titles:
            print(val)
        raise MyException(titles, "Didn't find window " + title)
    elif len(hwnd) > 1:
        for val in titles:
            print(val)
        raise MyException(titles, "Found too many windows " + title)
    return hwnd[0]

def enumHandler(hwnd, args):
    lParam, titles, title = args
    if win32gui.IsWindowVisible(hwnd):
        if "Idling" in title:
            titles.append(win32gui.GetWindowText(hwnd))
        if title.lower() == win32gui.GetWindowText(hwnd).lower():
            lParam.append(hwnd)

class MyException(Exception):
    pass

def sleepUntil(endTime):
    sleepTime = max(endTime - time.time(), 0)
    sleep(sleepTime)

def getInput(msg):
    forWin = win32gui.GetForegroundWindow()
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(findWindowHandle())

    inp = input(msg)
    if forWin > 0:
        win32gui.SetForegroundWindow(forWin)
    return inp

def positionWindows(topmost, x, y, cx, cy, move, size, irtgWIndow, changeTopMost = True):
    hwnd = findWindowHandle()
    if topmost and changeTopMost:
        topmost = win32con.HWND_TOPMOST
    elif changeTopMost:
        topmost = win32con.HWND_NOTOPMOST

    if move:
        move = 0
    else:
        move = win32con.SWP_NOMOVE

    if size:
        size = 0
    else:
        size = win32con.SWP_NOSIZE

    win32gui.SetWindowPos(hwnd, topmost, x, y, cx, cy, move + size)
    
    if irtgWIndow:
        win32gui.SetForegroundWindow(findWindowHandle("Idling to Rule the Gods"))
    
    sleep(0.1)
    return

def __playSound(duration = 1):
    duration = max(duration, 1)
    winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)
    sleep(duration)
    __endSound()

def __endSound():
    winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS | winsound.SND_PURGE)

def formatTime(duration, timeAt = False):
    if timeAt:
        futureTime = (datetime.datetime.now() + datetime.timedelta(seconds=duration))
        return datetime.datetime.strftime(futureTime, '%I:%M:%S %p')
    else:
        length = str(datetime.timedelta(seconds=duration)).split(':')
        retDur = ''
        if int(length[0]) > 0:
            retDur = '%02dh ' % int(length[0])
        if int(length[1]) > 0:
            retDur += '%02dm ' % int(length[1])
        if int(float(length[2])) > 0:
            retDur += '%02ds' % float(length[2])
        if retDur == '':
            retDur = '00s'
        return retDur.strip()

def soundOffIn(duration, soundLength = 5):
    print("Sounding off in:", formatTime(duration), "At:", formatTime(duration, True))
    Timer(duration, __playSound, [soundLength]).start()