import pyautogui as py
import win32gui
import sys
import time
import atexit
import re
import zmq
from time import sleep
from utils import clicky
from utils import movey
from utils import takeAndReadImage
from utils import detectKeypress
from utils import getInput
from utils import soundOffIn
from utils import findWindowHandle
from utils import sleepUntil
from utils import hotkeyPress
from utils import keyPress

class Move:
    def __init__(self, cap, uses, coords, cd, avail):
        self.startCap = cap
        self.uses = uses
        self.coords = coords
        self.coolDown = cd
        self.nextUse = time.time()
        self.avail = avail
        
    def useMove(self):
        if self.avail and self.readyUse(): # and py.pixelMatchesColor(*self.coords, (9, 9, 9), tolerance=10):
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

def setUses(skills):
    showTooltips = takeAndReadImage(670, 530, 710, 570)
    if showTooltips == 'OFF':
        clicky(660, 550)
    for key in skills:
        skill = skills[key]
        if skill.avail:
            x, y = skill.coords
            try:
                movey(x, y)
                uses = takeAndReadImage(x - 382, y - 36, x - 290, y - 16)
                uses = re.sub(r"[ ‘.]", "", uses)
                if uses != '':
                    skills[key].uses = int(uses)
            except ValueError:
                try:
                    movey(x, y)
                    uses = takeAndReadImage(x - 382, y - 36, x - 310, y - 16)
                    uses = re.sub(r"[ ]", "", uses)
                    if uses != '':
                        skills[key].uses = int(uses)
                except ValueError:
                    logging.debug(uses)
                    raise
    clicky(660, 550)
    saveSkills(skills)
    return skills

def orderSkills(skills):
    skillNames = []
    coolDowns = []
    for key in skills:
        coolDowns.append(skills[key].coolDown)
        skillNames.append(key)

    order = []
    notPriority = []
    while len(coolDowns) > 0:
        indx = coolDowns.index(max(coolDowns))
        key = skillNames[indx]
        if skills[key].needUse():
            order.append(skillNames.pop(indx))
        else:
            notPriority.append(skillNames.pop(indx))
        del coolDowns[indx]

    fb = 'Focused Breathing'
    if fb in notPriority:
        order.append(fb)
        notPriority.remove(fb)

    order.extend(notPriority)
    return order

def determineAvailSkills(skills, startPos = '', reverse = False):
    for key in skills:
        skills[key].avail = True

    [left, top, width, height, incWidth, incHeight] = (1682, 952, 71, 29, 322, 59)
    count = 0

    if reverse:
        skillList = list(reversed(list(skills)))
        incWidth *= -1
        incHeight *= -1
        left += incWidth * 3
        top += incHeight * 6
    else:
        skillList = list(skills)
    
    cont = False
    read = True
    for key in skillList:
        if key in startPos or startPos == '' or cont:
            if read:
                text = takeAndReadImage(left, top, left + width, top + height)
            #if key == 'Transformation Aura':
            #    from utils import takeImage
            #    takeImage(left, top, left + width, top + height).show()
            #    input('blah')
            if '7' in text: # or len(text) == 7:
                skills[key].avail = False
                if reverse:
                    read = False
                    cont = True
            else:
                if reverse:
                    cont = True
                else:
                    break
        if count == 3:
            count = 0
            left += (incWidth * 3)
            top -= incHeight
        else:
            count += 1
            left -= incWidth

    return skills

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

def detectEndFight(skills, fightButtonCoords, nextSkill):
    evts = poller.poll(1)
    if len(evts) > 0 :
        msg = socket.recv_string()
        if msg.lower == "stop":
            while msg.lower != "run":
                sleep(5)
                msg = socket.recv_string()

    movey(900, 75)
    # Finish Button
    text = takeAndReadImage(1044, 393, 1117, 417)
    if text == 'Finish':
        clicky(1021, 407)
        movey(900,0)
        sleep(0.5)
        sleepTime = 0
        for key in skills:
            skills[key].nextUse = time.time()

        if nextSkill != '':
            skills = determineAvailSkills(skills, nextSkill, True)
            nextSkill = ''
            for key in skills:
                if not skills[key].avail:
                    nextSkill = key
                else:
                    break

    # Shadow Clones button
    text = takeAndReadImage(660, 379, 1020, 429)
    if text == 'Fight Shadow Clones':
        clicky(*fightButtonCoords)
        movey(900,0)
        sleep(0.5)
        sleepTime = 0

    return skills, nextSkill

def useSkills(fightWhat):
    idleGodshwdn = findWindowHandle("Idling to Rule The Gods")
    skills = determineAvailSkills(loadSkills())
    fightButtonCoords = {'Clones': (991, 406), 'Jacky Lee': (1245, 400), 'Cthulhu': (1655, 405), 'Doppelganger': (845, 475), 'D. Evelope': (1245, 470), 'gods': (1640, 470)}
    
    if len(sys.argv) <= 1:
        answer = getInput("Do you wish to update the number of uses per skill?  y/n \n")
        if answer == 'y':
            skills = setUses(skills)
    
    while True:
        focus = getInput("Focus defeating 1) enemy or 2) using non-one cloned skills\n")
        if focus != '1' and focus != '2':
            print('Invalid choice, choose 1 or 2')
        else:
            break

    nextSkill = ''
    for key in skills:
        if not skills[key].avail:
            nextSkill = key
        else:
            break
    
    atkDelay = 0.25
    if focus == '1':
        skillsToUse = ['Shadow Fist', 'Invisible Hand', 'Big Bang', 'Unlimited Creation Works', 'Aura Ball', 'High Kick', 'Ionioi Hero Summon', 'Whirling Foot', '108 Fists', 'Double Punch']
        ignore = skillsToUse.copy()
    else:
        skillsToUse = orderSkills(skills)
        ignore = []

    # Shadow Clones button
    if py.pixelMatchesColor(991, 406, (3, 3, 3), tolerance=10):
        clicky(*fightButtonCoords[fightWhat])

    coolDowns = [time.time()] * len(skillsToUse)
    while True:
        if detectKeypress():
            break
        if py.pixelMatchesColor(1151, 405, (4, 4, 4), tolerance=10):
            skills[key].uses -= 1
            if min(coolDowns) >= time.time():
                sleep(min(coolDowns) - time.time() + 0.5)
            skills, nextSkill = detectEndFight(skills, fightButtonCoords[fightWhat], nextSkill)
        if win32gui.GetForegroundWindow() != idleGodshwdn:
            win32gui.SetForegroundWindow(idleGodshwdn)
        for x in range(len(skillsToUse)):
            key = skillsToUse[x]
            if key in skills and skills[key].useMove():
                coolDowns[x] = skills[key].nextUse
                sleepTime = max(min(coolDowns) - time.time() + 0.3, atkDelay)
                if 'focused' not in key.lower() and key not in ignore and not skills[key].needUse():
                    ignore.append(key)
                    skillsToUse.append(key)
                    skillsToUse.remove(key)
                sleep(sleepTime)
                break
            else:
                if key not in skills:
                    print("Key:", key, "not in skills")
                elif skills[key].nextUse < time.time() and skills[key].avail:
                    print("Skill:", key, "off cooldown but not able to be used")
    saveSkills(skills)
    atexit.unregister(saveSkills)
    return ''

def training(startLevel = 500):
    skills = loadSkills()
    order = list(reversed(list(skills.keys())))
    first = True
    level = 500
    
    for x in range(len(order)):
        mousePos = py.position()
        if x < len(order) - 1:
            key = order[x + 1]
            skill = skills[key]
            #indx = order.index(key)
            cloneCount = max(skill.startCap - (skill.uses // 3), 1)
        
        if level < startLevel:
            level += 500
            lastCloneCount = cloneCount
            continue
        
        forWin = win32gui.GetForegroundWindow()
        win32gui.SetForegroundWindow(findWindowHandle("Idling to Rule the Gods"))
        sleep(0.1)
        clicky(900, 75)
        keyPress("6")

        if first:
            clicky(1500, 460)
            first = False
            sleep(0.1)
            sleepTime = time.time()
        clicky(1540, 304)
        movey(*mousePos)
        hotkeyPress("ctrl", "a")
        keyPress(str(level))
        
        if cloneCount > 1:
            print(cloneCount, cloneCount - lastCloneCount)
            clicky(990, 250)
            movey(*mousePos)        
            hotkeyPress("ctrl", "a")
            cloneCount = max(cloneCount, lastCloneCount + 1)
            keyPress(cloneCount - lastCloneCount + 1)
            sleep(10)

        win32gui.SetForegroundWindow(forWin)
        
        if x == 27:
            break
        
        sleepTime += level * 30 / 1000
        soundOffIn(sleepTime - time.time() - 5)
        sleepUntil(sleepTime)
        
        if x == 26:
            level = 9500
        
        lastCloneCount = cloneCount
        level += 500
        
    return ''

def theBaalSlayer():
    pyPause = py.PAUSE
    py.PAUSE = 0
    imgs = {'feet': 'feet.png', 'mouth': 'mouth.png', 'tail': 'tail.png', 'wings': 'wings.png'}
    btnLocs = {'eyes': (751, 473), 'feet': (1351, 931), 'mouth': (1611, 592), 'tail': (851, 948), 'wings': (711, 642)}
    scanRegions = {'feet': (1280, 854, 300, 34), 'mouth': (1700, 515, 34, 300), 'tail': (780, 871, 300, 33), 'wings': (800, 565, 34, 300)}
    #for key in imgs:
    #    clicky(*btnLocs[key])

    while True:
        if detectKeypress():
            break
        loc = py.locateOnScreen(imgs['mouth'], region=scanRegions['mouth'], grayscale=True, confidence=0.99)
        if loc is not None:
            py.click(*btnLocs['mouth'])
            sleep(.1)
        #for key in imgs:
        #    if py.locateOnScreen(imgs[key], region=scanRegions[key]) is not None:
        #        clicky(*btnLocs[key])
        #        break
    py.PAUSE = pyPause
    return ''

def something():
    conf = 0.999
    for x in range(10):
        locs = py.locateAllOnScreen("C:\\Users\\Logan\\source\\repos\\IdleGods\\IdleGods\\temp.png", grayscale=True, confidence=conf)
        locs = list(locs)
        for loc in locs:
            print(loc, conf)
        if len(locs) == 5:
            for loc in locs:
                print(py.center(loc))
            break
        conf -= 0.01

socket = zmq.Context().socket(zmq.REP)
socket.connect("tcp://127.0.0.1:5555")
poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)
            