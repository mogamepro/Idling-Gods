import os
import datetime
import sys
import ctypes
import logging
import win32gui
import win32con
import time
import zmq
import skillControl
import pets
import creations
import afky
import buildings
import utils
import pyautogui as py
from time import sleep

def launchAfky(*args):
    positionWindows(True, 0, 0, 770, 332, True, False, True)
    return afky.runAfky()

def launchUseSkills(*args):
    try:
        forWin = win32gui.GetForegroundWindow()
        utils.positionWindows(False, 0, 0, 770, 332, True, False, True)
        choices = {'1': "Clones", '2': "Jacky Lee", '3': "Cthulhu", '4': "Doppelganger", '5': "D. Evelope", '6': "gods"}
        if len(args) > 1:
            choice = args[1]
        else:
            choice = ''
            while choice == '':
                choice = utils.getInput("Fight: " + ', '.join([') '.join([k, v]) for k, v in choices.items()]) + '\n')
        return skillControl.useSkills(choices[choice])
    except OSError:
        try:
            skills
            skillControl.saveSkills(skills)
        except UnboundLocalError:
            pass
        logging.getLogger(__name__).exception("Program terminated")
        print("Restarting script")
        os.execl(sys.executable, sys.argv[0], sys.argv[0], '2', choice)
    return ''

def launchCalcCreations(*args):
    creation = utils.getInput('Which creation?\n').lower()
    num = eval(utils.getInput('How many?\n'))
    return creations.create(creation, num)

def launchCalcPets(*args):
    utils.positionWindows(False, 0, 0, 0, 0, True, False, True)
    while True:
        choice = utils.getInput("1) Pet Hunger  2) Pet Clone Stats")
        if choice == '1':
            return pets.petHunger()
        elif choice == '2':
            return pets.petClone()

def launchCalcDivGen(*args):
    buildings.divUpgrade()
    return ''

def launchCalcBestMonumentPath(*args):
    return buildings.bestMonumentPath()

def launchSkillTraining(*args):
    utils.positionWindows(False, 0, 0, 0, 0, True, False, False)
    level = utils.getInput("Start at how many clones? Blank for 500\n")
    if level == "":
        return skillControl.training()
    level = eval(level)
    if isinstance(level, int) and level % 500 == 0:
        return skillControl.training(int(level))
    else:
        print("Invalid level")
        choice = ''

def askChoice(*args):
    choices = {'1': launchAfky, '2': launchUseSkills, '3': launchCalcCreations, '4': launchCalcPets, '5': launchCalcDivGen, '6': launchCalcBestMonumentPath, '7': launchSkillTraining, 'q': sys.exit}
    choice = args[0]

    while True:
        utils.positionWindows(False, 0, 0, 770, 332, False, True, False)
        if choice == '' or choice is None:
            choice = utils.getInput('Choose: 1) Afky, 2) Use Skills, 3) Calc creation, 4) Pet Clone Stat calc\n        5) Div Gen, 6) Monument Path, 7) Skill Training, or q) Exit\n')
        if choice in choices.keys():
            if len(args) == 1:
                choice = choices[choice]()
            else:
                choice = choices[choice](*args)
        else:
            print("Invalid selection. Choose:", ', '.join([k for k in choices.keys()]))
            choice = ''
    return

if __name__ == "__main__":
    fileName = 'Error Logs/Error Log - ' + datetime.datetime.strftime(datetime.datetime.now(), '%I_%M_%S_%p') + '.log'
    logging.basicConfig(filename=fileName, level=logging.DEBUG, filemode='w')
    try:
        if False:
            import gui
            gui.MainWindow().run()
        else:
            start = time.time()
            ctypes.windll.kernel32.SetConsoleTitleW("Idle Gods Controller X")
            args = [''] * len(sys.argv)
            if len(sys.argv) > 1:
                for x in range(1, len(sys.argv)):
                    args[x - 1] = sys.argv[x]
            askChoice(*args)
    except SystemExit:
        pass
    except BaseException:
        logging.getLogger(__name__).exception("Program terminated")
        logging.debug("Ran for: " + utils.formatTime(int(time.time() - start)))
        raise
    logging.shutdown()