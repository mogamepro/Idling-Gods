from utils import formatNumber

def addCreation(creation, num, creations):
    creations[creation]['amt'] += num
    for key in creations[creation]:
        if key != 'amt':
            creations = addCreation(key, creations[creation]['amt'] * creations[creation][key], creations)
    return creations

def create(top, num):
    creations = {
        'light' : {'amt' : 0},
        'stone' : {'amt' : 0},
        'soil' : {'stone' : 1, 'amt' : 0},
        'air' : {'light' : 2, 'amt' : 0},
        'water' : {'air' : 3, 'amt' : 0},
        'plant' : {'soil' : 2, 'water' : 2, 'amt' : 0},
        'tree' : {'soil' : 5, 'water' : 3, 'amt' : 0},
        'fish' : {'water' : 10, 'plant' : 5, 'amt' : 0},
        'animal' : {'water' : 15, 'plant' : 9, 'fish' : 3, 'amt' : 0},
        'human' : {'water' : 100, 'plant' : 25, 'fish' : 25, 'animal' : 15, 'amt' : 0},
        'river' : {'water' : 5000, 'amt' : 0},
        }
    addCreation(top, num, creations)
    for key in creations.keys():
        if creations[key]['amt'] > 0 :
            print(key, ' ', formatNumber(creations[key]['amt']))
    return ''
