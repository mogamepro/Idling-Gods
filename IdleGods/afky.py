from time import sleep
from utils import clicky
from utils import parseNum
from utils import readImage
from utils import takeImage
from utils import detectKeypress

class Afky:
    pass

def getStat(stat):
    try:
        imCoords = {speed: (335, 400, 605, 435), power: (335, 450, 605, 485), hp: (335, 500, 605, 535), count: (335, 550, 605, 585), exp: (335, 600, 605, 635)}
        im = takeImage(*imCoords[stat])
        parseNum(readImage(im))
    except ValueError:
        print("This is area attempted to read")
        im.show()
        raise ValueError

def runAfky():  #TODO: Refactor
    clickCoords = {speed: (750, 415), power: (650, 520), hp: (650, 570), count: (1245, 470)}
    stats = {speed: 0, power: 0, hp: 0, count: 0, exp: 0}
    
    for key in stats:
        stats[key] = getStat(key)
    
    while True:
        if detectKeypress():
            return ''

        stats['exp'] = getStat('exp')
        hpExp = (stats['hp'] ** 2 * 100) // 3
        countExp = count ** 2 * 100

        #hpExp + capExp if (hp better than count) else countExp + capExp
        temp = (hpExp + (count * (hp * count * 2 + count) / 2)) if (hpExp / (count ** 0.9) < countExp / (hp ** 1.1)) else (countExp + (hp * (hp * count * 2 + hp) / 2))
        #print(hpExp / (count ** 0.9) < countExp / (hp ** 1.1), ' ', temp)
        #True if exp >= above else False
        #print(True if exp > temp else False)
        neededExp = (hpExp + (count * (hp * count * 2 + count) / 2)) if hpExp / (count ** 0.9) < countExp / (hp ** 1.1) else (countExp + (hp * (hp * count * 2 + hp) / 2))
        print('Exp:', exp, 'hp:', hp, 'hp exp:', hpExp, 'count:', count, 'count exp:', countExp, 'Needed Exp:', neededExp)
        while exp < neededExp:
            if detectKeypress():
                return ''
            exp = parseNum(readImage(takeImage(335, 600, 605, 635)))
            sleep(1)
        check = True if (exp >= neededExp) else False
        while check:
            if detectKeypress():
                return ''
            if hp > 40 and (hp + count) * 10 > speed < 3800 and exp >= (hp + count) * 10 - speed * ((hp + count) * 10 - speed + 1) / 2:
                clicky(*coords[0])
                exp = exp - ((hp + count) * 10 - speed * ((hp + count) * 10 - speed + 1) / 2)
                speed += 10
            elif hpExp / (count ** 0.9) < countExp / (hp ** 1.1):
                if count == hp == 1:
                    capExp = 1
                else:
                    capExp = (count * (hp * count * 2 + count) / 2)
                if hpExp + capExp <= exp:
                    clicky(*coords[2])
                    clicky(*coords[4])
                    exp = exp - hpExp - capExp
                    hp += 1
                else:
                    break
            elif countExp / (hp ** 1.1) < hpExp / (count ** 0.9):
                if count == hp == 1:
                    capExp = 1
                else:
                    capExp = (hp * (hp * count * 2 + hp) / 2)
                if countExp + capExp <= exp:
                    clicky(*coords[3])
                    clicky(*coords[4])
                    exp = exp - countExp - capExp
                    count += 1
                else:
                    break
            else:
                break
            hpExp = (hp ** 2 * 100) // 3
            countExp = count ** 2 * 100
            neededExp = (hpExp + (count * (hp * count * 2 + count) / 2)) if hpExp / (count ** 0.9) < countExp / (hp ** 1.1) else (countExp + (hp * (hp * count * 2 + hp) / 2))
            check = True if (exp >= neededExp) else False
    return ''
