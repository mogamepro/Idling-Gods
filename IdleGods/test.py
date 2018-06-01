import pyscreeze
import datetime
import logging
import time
import sys
from ctypes import windll
import pyautogui as py

def pixel(x, y):
    if sys.platform == 'win32':
        # On Windows, calling GetDC() and GetPixel() is twice as fast as using our screenshot() function.
        hdc = windll.user32.GetDC(0)
        color = windll.gdi32.GetPixel(hdc, x, y)
        # color is in the format 0xbbggrr https://msdn.microsoft.com/en-us/library/windows/desktop/dd183449(v=vs.85).aspx
        r = color % 256
        g = (color // 256) % 256
        b = color // (256 ** 2)
        windll.user32.ReleaseDC(0, hdc)
        return (r, g, b)
    else:
        return screenshot().getpixel((x, y))

pyscreeze.pixel = pixel

def formatTime(duration):
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


fileName = 'Error Logs\\Troubleshooting Log - ' + datetime.datetime.strftime(datetime.datetime.now(), '%I_%M_%S_%p') + '.log'
logging.basicConfig(filename=fileName, level=logging.DEBUG, filemode='w')
logging.debug("py screenshot and pixel match")
logging.debug(sys.version)
logging.debug(sys.version_info)

try:
    x = 0
    start = time.time()
    while True:
        pyscreeze.pixelMatchesColor(991, 406, (3, 3, 3), tolerance=10)
        pyscreeze.screenshot()
        x += 1
        print(x, formatTime(int(time.time() - start)),  end='\r')
except BaseException as e:
    logging.getLogger(__name__).exception("Program terminated")
    logging.debug("Ran for: " + formatTime(int(time.time() - start)))
    input("Errored %s" % e)
    raise
    
logging.shutdown()

from pyscreeze import _locateAll_python
from pyscreeze import _locateAll_opencv
import pyscreeze
list(pyscreeze._locateAll_python("C:\\Users\\Logan\\Desktop\\blah\\needle.PNG", "C:\\Users\\Logan\\Desktop\\blah\\haystack.PNG"))