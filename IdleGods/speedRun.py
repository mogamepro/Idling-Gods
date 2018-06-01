import utils
from skillControl import loadSkills
from time import sleep

def startSkillTraining(skills):
    utils.clicky(900, 75)
    utils.keyPress("6")
    utils.clicky(990, 250)
    utils.hotkeyPress("ctrl", "a")
    cloneCount = skills['Teleport'].startCap - skills['Teleport'].uses // 3
    utils.keyPress(cloneCount)
    utils.clicky(1500, 460)
    return

def fighting(): # TODO: Check if fighting going on, ensure combat is going best target
    pass

def buildDivGen():
    utils.clicky(900, 75)
    utils.keyPress("1")
    if utils.takeAndReadImage(1571, 418, 1769, 449) == "Change creation":
        utils.clicky(1571, 418)
    utils.clicky(1000, 260)

    for x in range(12):
        utils.keyPress('tab')
        utils.keyPress(5)

    utils.clicky(1591, 615)

    text = utils.takeAndReadImage(1733, 245, 1766, 262)
    if text != "ON" and text != "0N":
        utils.clicky(1749, 253)

    text = utils.takeAndReadImage(1733, 290, 1766, 307)
    if text != "ON" and text != "0N":
        utils.clicky(1749, 298)

    while utils.takeAndReadImage(721, 395, 892, 421) != "Shadow clone":
        sleep(1)

    utils.keyPress(2)
    utils.clicky(1600, 463)
    return

def main():
    startSkillTraining(loadSkills())
    fighting()
    buildOneMonuments()