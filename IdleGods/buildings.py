import os
from utils import detectKeypress
from utils import soundOffIn

class Building:
    def __init__(self, baseDivCost, baseBuildTime, baseMult, baseUpgradeDivCost, baseUpgradeBuildTime, physical = True, mystical = True, battle = True, creation = True):
        self.level = 1
        self.upgradeLevel = 0
        self.baseBuildTime = baseBuildTime
        self.baseUpgradeBuildTime = baseUpgradeBuildTime
        self.baseDivCost = int(baseDivCost)
        self.baseUpgradeDivCost = baseUpgradeDivCost
        self.baseMult = baseMult
        self.rebirthMult = self.upgradeLevel / 5
        self.rebirthMod = self.baseMult * self.level * self.upgradeLevel
        self.nextLevelCost = self.baseDivCost
        self.baseUpgradeDivCost = self.baseUpgradeDivCost
        self.nextLevelBuildTime = self.baseBuildTime * (self.level + 1)
        self.nextUpgradeBuildTime = self.baseUpgradeBuildTime
        self.physical = physical
        self.mystical = mystical
        self.battle = battle
        self.creation = creation
        
    def levelUp(self):
        self.level += 1
        self.nextLevelBuildTime = self.baseBuildTime * (self.level + 1)
        self.nextLevelCost = self.baseDivCost * self.level
        self.rebirthMod = self.baseMult * self.level * self.rebirthMult

    def upgrade(self):
        self.upgradeLevel += 1
        self.nextUpgradeBuildTime = self.baseUpgradeBuildTime * (self.upgradeLevel + 1)
        self.nextUpgradeCost = self.baseUpgradeDivCost * max(self.upgradeLevel, 1) ** 2
        self.rebirthMult = min(self.upgradeLevel * 0.25, 5)
        self.rebirthMod = self.baseMult * self.level * self.rebirthMult

    def nextRebirthMod(self, levelOrUpgrade):
        if levelOrUpgrade == 'level':
            mod = self.baseMult * (max(self.level, 1) + 1) * max(self.rebirthMult, 0.25)
        elif levelOrUpgrade == 'upgrade':
            mod = self.baseMult * max(self.level, 1) * min(self.rebirthMult + 0.25, 5)
        cnt = 1
        for stat in [self.physical, self.mystical, self.battle, self.creation]:
            if not stat:
                cnt += 1
        return mod / cnt

def bestMonumentPath():
    monuments = {
        'mightyStatue' : Building(12.5e6, 120, 1, 2.5e9, 60, True, False, False, False),
        'mysticGarden' : Building(73.8e6, 720, 6, 12.2e9, 360, False, True, False, False),
        'tombOfGods' : Building(360.1e6, 3600, 30, 79.44e9, 1800, False, False, True, False),
        'lighthouse' : Building(1.875e9, 36000, 150, 1.996e12, 9000, False, False, False, True),
        'godlyStatue' : Building(5.405e9, 60000, 200, 5.746e12, 15000),
        'pyramidOfPower' : Building(11.46e9, 75000, 600, 30.73e12, 37500),
        'templeOfGod' : Building(20.2e9, 150000, 1500, 51.54e12, 75000)
    }

    lvlUPgrade = []
    while True:
        next, doWhat = nextBest(monuments)
        if next not in lvlUPgrade:
            lvlUPgrade.append(next)
        if doWhat == 'level':
            monuments[next].levelUp()
            print("Level:   ", next, "to: ", monuments[next].level)
        else:
            monuments[next].upgrade()
            print("Upgrade: ", next, "to: ", monuments[next].upgradeLevel)
        input("Press enter to continue")
        os.system('cls') or None
        if detectKeypress():
            break

    for key in lvlUPgrade:
        print(key, "level:", monuments[key].level, "upgrade:", monuments[key].upgradeLevel)
    
    return ''

def nextBest(monuments):
    best = [9e25, '', '']
    for key in monuments:
        build = monuments[key]
        lvlMod = build.nextLevelBuildTime / (build.nextRebirthMod('level') - build.rebirthMod)
        upMod = build.nextUpgradeBuildTime / (build.nextRebirthMod('upgrade') - build.rebirthMod) if build.upgradeLevel < 20 else 9e25
        if lvlMod > 0 and upMod > lvlMod < best[0]:
            best[0] = lvlMod
            best[1] = key
            best[2] = 'level'
        elif upMod > 0 and (lvlMod > upMod < best[0] or upMod == lvlMod < best[0]):
            best[0] = upMod
            best[1] = key
            best[2] = 'upgrade'
    best.pop(0)
    return best

class DivinityGenerator:
    def __init__(self):
        self.baseDivC = 2
        self.baseConSec = 10
        self.baseUpgradeTime = 1000000
        self.divGain = 0
        self.divSpeed = 0
        self.divEachCon = self.baseDivC + self.divGain
        self.conSec = self.baseConSec * (self.divSpeed + 1)

    def nextUpgrade(self):
        nextGain = self.nextBuildTime(self.divGain) / (self.conSec * self.nextDivEachCon())
        nextSpeed = self.nextBuildTime(self.divSpeed) / (self.nextConSec() * self.divEachCon)
        if nextGain < nextSpeed:
            self.divEachCon = self.nextDivEachCon()
            self.divGain += 1
            yield("Divinity Gain to: " + str(self.divGain))
        else:
            self.conSec = self.nextConSec()
            self.divSpeed += 1
            yield("Converting Speed to: " + str(self.divSpeed))

    def nextDivEachCon(self):
        return self.baseDivC + self.divGain + 1

    def nextConSec(self):
        return self.baseConSec * (self.divSpeed + 2)

    def nextBuildTime(self, level):
        buildTime = max(self.baseUpgradeTime * (2 * level), self.baseUpgradeTime)
        return buildTime

def divUpgrade():
    divGen = DivinityGenerator()
    steps = []

    while True:
        steps.append(next(divGen.nextUpgrade()))
        os.system('cls') or None
        for step in steps:
            print(step)
        input("Press enter to continue")

def buildingTimer(baseBuildTime, level, cloneCount, buildSpeed):
    duration = baseBuildTime * level * (1000 / cloneCount) / (buildSpeed / 100 + 1)
    soundOffIn(duration, 5)