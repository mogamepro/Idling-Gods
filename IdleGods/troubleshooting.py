import atexit
import pytesseract
import pyautogui as py
import time
import win32api
import win32con
import sys
import logging
import datetime
from time import sleep
from PIL import ImageGrab

def clicky(*coords):
    movey(*coords, .1)
    py.click(*coords)

def movey(x, y, duration = 0.1):
    py.moveTo(x, y, duration)

def detectKeypress():
    if win32api.GetAsyncKeyState(win32con.VK_CONTROL):
        sys.exit()
    elif win32api.GetAsyncKeyState(win32con.VK_SHIFT):
        return True
    elif win32api.GetAsyncKeyState(win32con.VK_MENU):
        input("Press enter to continue\r")
    return False

def detectEndFight(skills, fightButtonCoords, fightWhat):
    # Finish Button
    text = takeAndReadImage(1044, 393, 1044 + 73, 393 + 24)
    if text == 'Finish':
        clicky(1021, 407)
        movey(900,0)
        sleep(0.5)
        sleepTime = 0
        for key in skills:
            skills[key].nextUse = time.time()

    # Shadow Clones button
    text = takeAndReadImage(660, 379, 660 + 360, 379 + 50)
    if text == 'Fight Shadow Clones':
        clicky(*fightButtonCoords[fightWhat])
        movey(900,0)
        sleep(0.5)
        sleepTime = 0

class Move:
    def __init__(self, cap, uses, coords, cd, avail):
        self.startCap = cap
        self.uses = uses
        self.coords = coords
        self.coolDown = cd
        self.nextUse = time.time()
        self.avail = avail
        
    def useMove(self):
        if self.avail and self.readyUse() and py.pixelMatchesColor(*self.coords, (9, 9, 9), tolerance=10):
            clicky(*self.coords)
            x, y = self.coords
            movey(x - 20, y)
            self.nextUse = time.time() + self.coolDown
            self.uses += 1
            return True
        else:
            return False

    def readyUse(self):
        return (time.time() >= self.nextUse)

    def needUse(self):
        return (self.uses / 3 < self.startCap)

def saveSkills(skills):
    with open('skills.txt', 'w') as f:
        for key in skills:
            skill = skills[key]
            line = key + '.' + str(skill.startCap) + '.' + str(skill.uses) + '.' + str(skill.coords) + '.' + str(int(skill.coolDown * 1000)) + '\n'
            f.write(line)

def loadSkills():
    skills = {}
    with open('skills.txt', 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            name, cap, uses, coords, cd = line.split('.')
            coords = (int(coords[1:coords.find(',')]), int(coords[coords.find(',') + 1 :].rstrip(')')))
            skills[name] = Move(int(cap), int(uses), coords, int(cd) / 1000, True)
    atexit.register(saveSkills, skills)
    return skills

def orderSkills():
    skills = loadSkills()
    
    skillNames = []
    unordered = []
    for key in skills:
        unordered.append(skills[key].coolDown)
        skillNames.append(key)

    order = []
    notPriority = []
    while len(unordered) > 0:
        indx = unordered.index(max(unordered))
        if skills[key].needUse():
            order.append(skillNames.pop(indx))
        else:
            notPriority.append(skillNames.pop(indx))
        del unordered[indx]

    fb = 'Focused Breathing'
    if fb in notPriority:
        order.append(fb)
        notPriority.remove(fb)

    order.extend(notPriority)
    return [skills, order]

def useSkills(skills, order, fightWhat):
    fightButtonCoords = {'Clones': (991, 406), 'Jacky Lee': (1245, 400), 'Cthulhu': (1655, 405), 'Doppelganger': (845, 475), 'D. Evelope': (1245, 470), 'gods': (1640, 470)}

    # Shadow Clones button
    if py.pixelMatchesColor(991, 406, (3, 3, 3), tolerance=10):
        clicky(*fightButtonCoords[fightWhat])
        sleep(0.5)

    tries = 0
    coolDowns = [time.time()] * len(order)
    ignore = []
    while True:
        if detectKeypress():
            saveSkills(skills)
            atexit.unregister(saveSkills)
            return ''

        for x in range(0, len(order)):
            key = order[x]
            if skills[key].useMove():
                tries = 0
                coolDowns[x] = skills[key].nextUse
                sleepTime = max(min(coolDowns) - time.time() + 0.3, 0.36)
                if 'focused' not in key.lower() and key not in ignore and not skills[key].needUse():
                    ignore.append(key)
                    order.append(key)
                    order.remove(key)
                sleep(sleepTime)
                break
            elif skills[key].nextUse < time.time():
                print("Skill:", key, "off cooldown but not able to be used")
        else:
            if min(coolDowns) >= time.time():
                sleep(min(coolDowns) - time.time() + 0.5)
            else:
                movey(900, 0, .2)
                sleepTime = 1
                
                detectEndFight(skills, fightButtonCoords, fightWhat)

                if tries > 5:
                    sleep(1)
                    return '2'
                else:
                    tries += 1
                
                sleep(sleepTime)
    return ''

def takeAndReadImage(left, top, right, bottom):
    return readImage(takeImage(left, top, right, bottom))

def takeImage(left, top, right, bottom):
    return ImageGrab.grab(bbox=(left, top, right, bottom))

def readImage(im):
    return pytesseract.image_to_string(im, config = '--psm 7')

if __name__ == "__main__":
    try:
        fileName = 'Error Logs\\Troubleshooting Log - ' + datetime.datetime.strftime(datetime.datetime.now(), '%I_%M_%S_%p') + '.log'
        logging.basicConfig(filename=fileName, level=logging.DEBUG, filemode='w')

        choices = {'1': "Clones", '2': "Jacky Lee", '3': "Cthulhu", '4': "Doppelganger", '5': "D. Evelope", '6': "gods"}
        choice = ''
        while choice == '':
            choice = input("Fight: " + ', '.join([') '.join([k, v]) for k, v in choices.items()]) + '\n')
        skills, order = orderSkills()
        useSkills(skills, order, choices[choice])
    except BaseException:
        logging.getLogger(__name__).exception("Program terminated")
        logging.debug("Ran for: " + utils.formatTime(int(time.time() - start)))
        raise
    logging.shutdown()