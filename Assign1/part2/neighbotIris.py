import numpy as np

#Colors
class bcolors:
    Green = '\033[92m'
    Red = '\033[91m'
    Yellow = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class DataPoint(object):
    x = 0.0
    y = 0.0
    type = 0

    def __init__(self, newX,newY, newType):
       self.x = newX
       self.y = newY
       self.type = newType

    def speak(self):
        print('found: ' + str(self.type) + ' at ' + str(self.x) + ', ' + str(self.y))

def findNearest(x, y, k, collection):
    best = [float('inf')] * k
    points = []
    for point in collection:
        best.sort()

        new = findLength(point.x, point.y, x, y)
        if(new < best[-1]):
            best[-1] = new
            points.append(point)
    points = points[-k:]
    # for point in points:
        # point.speak()
    return points

def findLength(x, y, x2, y2):
    return np.sqrt(pow((x2 - x), 2) + pow((y2 - y), 2))

def createCollection(trainerData):
    collection = []
    for data in trainerData:
        list = data.split(' ')
        collection.append(DataPoint(float(list[0]),float(list[1]),int(list[2])))
    return collection

def guess(datapoint, k, collection):
    near = []
    for point in findNearest(datapoint.x,datapoint.y,k,collection):
        near.append(point.type) 
    return max(set(near), key=near.count)

def parse(filePath):
    ret = []
    f = open(filePath, 'r')
    for line in f.read().split('\n'):
        ret.append(line)
    del ret[-1]
    return ret

def runTest(k, trainingSet, testSet):
    trainerData = parse(trainingSet)
    collectionTrain = createCollection(trainerData)

    testData = parse(testSet)
    # collectionTest = createCollection(testData)


    hits = 0.0
    miss = 0.0
    tries = 0.0
    for testPoint in createCollection(testData):
        guessPoint = guess(testPoint, k, collectionTrain)
        if(guessPoint == testPoint.type):
            hits += 1
            # print(bcolors.Green + "HIT!  guessing: " + str(guessPoint) + " was: " + str(testPoint.type) + bcolors.ENDC)
        else:
            miss += 1
            # print(bcolors.Red + "MISS! guessing: " + str(guessPoint) + " was: " + str(testPoint.type) + bcolors.ENDC)
        tries += 1
    print("\nJobs done, with " + str(k) + " neighbors")
    print("Hit " + str(hits) + " times. Missed " + str(miss) + " times")
    ratio = hits/tries * 100
    if ratio > 70:
        color = bcolors.Green
    elif ratio < 65:
        color = bcolors.Red
    else:
        color = bcolors.Yellow
    print(color + "Hit ratio was " + str(hits/tries * 100) + "%" + bcolors.ENDC)


if __name__ == '__main__':

    # Constants
    # k = 7
    trainingSet = 'IrisTrain2014.dt'
    # trainingSet = 'IrisTest2014.dt'
    # testSet     = 'IrisTrain2014.dt'
    testSet     = 'IrisTest2014.dt'

    for k in range(1,10): 
        runTest(k, trainingSet, testSet)
