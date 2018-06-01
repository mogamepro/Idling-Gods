from utils import readImage
from utils import takeImage
from utils import clicky
from utils import hotkeyPress
from utils import keyPress
from utils import formatTime
from utils import movey
from utils import soundOffIn

def petClone():
    coords = [(935, 590), (935, 660), (935, 730)]
    petMystic = eval(readImage(takeImage(951, 921, 1142, 955)))
    petBattle = eval(readImage(takeImage(951, 957, 1142, 991)))
    cloneStats = [
        int(max(petBattle * 23 / 11000, 1)),     # clonePhysical
        int(petBattle * 20 // 33),               # cloneMystic
        int(petMystic * 1.1 // 2)                # cloneBattle
    ]
    
    #if cloneStats[1] > 50 < cloneStats[2]:
    #    cloneStats[0] = 2

    for x in range(len(coords)):
        clicky(*coords[x])
        hotkeyPress("ctrl", "a")
        keyPress(cloneStats[x])
    
    clicky(1400, 830)
    return ''

def petHunger(currentHunger = 0):
    if currentHunger == 0:
        movey(970, 335)
        currentHunger = float(readImage(takeImage(540, 555, 595, 575)))
    hungerSecond = 100 / (12 * 60 * 60)
    to75 = max(currentHunger - 75, 0)
    to50 = max(currentHunger - 50, 0)
    to10 = max(currentHunger - 10, 0)

    for x in [to10, to50, to75]:
        if x > 0:
            print(formatTime(x / hungerSecond))
            tim = x

    soundOffIn(tim / hungerSecond)