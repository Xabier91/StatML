import numpy as np
import operator
import sys
import time

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

def roundTuple((x,y)):
    return (round(x,1), round(y,1))


def findMeans(collection):
    pairs = [(0,0), (0,0), (0,0)]
    totals = [0,0,0]
    listsx = [[],[],[]]
    listsy = [[],[],[]]
    for pair in collection:
        pairs[pair.type] = tuple(map(operator.add, pairs[pair.type], (pair.x,pair.y)))
        totals[pair.type] += 1
        listsx[pair.type].append(pair.x)
        listsy[pair.type].append(pair.y)
    i = 0
    while(i < len(pairs)):
        (accX, accY) = pairs[i]
        pairs[i] = (accX/totals[i], accY/totals[i], np.std(listsx[i]), np.std(listsy[i]))
        print ("Type " + str(i) + " has a mean of (" + str(accX/totals[i])    + ", " + str(accY/totals[i])    + ")." 
                                + " An std of ("     + str(np.std(listsx[i])) + ", " + str(np.std(listsy[i])) + ").")
        i += 1
    print "Overall mean is " + str(findMean(collection)) + " and overall std is " + str(findStds(collection))
    return pairs

def findMean(collection):
    # 3 is the number of types we have in the dataset
    accX = 0
    accY = 0
    for point in collection:
        accX += point.x
        accY += point.y
    return (accX/len(collection), accY/len(collection))

def findStds(collection):
    xList = []
    yList = []
    for point in collection:
        xList.append(point.x)
        yList.append(point.y)
    return (np.std(xList), np.std(yList))

def printAndNormalize(trainingCollection, testCollection):
    (meanx, meany) = findMean(trainingCollection)
    (stdx, stdy) =  findStds(trainingCollection)

    meansAndStds = findMeans(trainingCollection)
    normalize((meanx,meany), (stdx, stdy), trainingCollection)

    normalize((meanx,meany), (stdx, stdy), testCollection)

def normalize(means, stds, collection):
    (meanX, meanY) = means
    (stdx, stdy) = stds
    for point in collection:
       point.x -= meanX 
       point.y -= meanY

       point.x = point.x/stdx
       point.y = point.y/stdy

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

def splitList(cutLength, list):
    return [list[x:x+cutLength] for x in xrange(0, len(list), cutLength)]

def runTest(k, trainingCollection, testCollection):
    hits = 0.0
    miss = 0.0
    tries = 0.0
    for testPoint in testCollection:
        guessPoint = guess(testPoint, k, trainingCollection)
        if(guessPoint == testPoint.type):
            hits += 1
        else:
            miss += 1
        tries += 1
    ratio = hits/tries * 100
    if ratio > 70:
        color = bcolors.Green
    elif ratio < 65:
        color = bcolors.Red
    else:
        color = bcolors.Yellow
    print("Hit ratio with " + str(k) + " was " + color + str(ratio) + "%." + bcolors.ENDC +
            " With " + str(tries) + " tries " + str(hits) + " hits and " + str(miss) +
          " misses")
    return (ratio, k)

def printTest(ratio, k, tries):
    if ratio > 70:
        color = bcolors.Green
    elif ratio < 65:
        color = bcolors.Red
    else:
        color = bcolors.Yellow
    print("Hit ratio with " + str(k) + " was " + color + str(ratio) + "%." + bcolors.ENDC +
            " With " + str(tries) + " tries " + str(ratio/100 * tries) + " hits and " + str(tries - ratio/100 * tries) +
          " misses")
    return (ratio, k)


def findBest(collection):
    bestRatio = 0
    bestK = 0
    for (curRatio,curK) in collection: 
        if(bestRatio < curRatio):
            (bestRatio, bestK) = (curRatio, curK)
    return (bestRatio, bestK) 

def printCollection(collection):
    for (ratio,k) in collection: 
        printTest(ratio, k)

def collect(k, trainingCollection, testCollection):
    ret = []
    for i in range(1,k+1): 
       (ratio, k) = runTest(i, trainingCollection, testCollection)
       ret.append((i, ratio))# runTest(i, trainingCollection, testCollection))) 
    return ret


if __name__ == '__main__':

    crossvalidate = False

    var = raw_input("Use cross? y/n\n")
    if(var == "y"):
        crossvalidate = True
        numOfCuts = int(raw_input("How many partitions?\n"))


    # Constants, k must be positive
    # k = 25

    # crossvalidation constants
    # numOfCuts = 5
    
    trainingSet = 'IrisTrain2014.dt'
    trainerData = parse(trainingSet)
    trainingCollection = createCollection(trainerData)
    # trainingSet = 'IrisTest2014.dt'
    # testSet     = 'IrisTrain2014.dt'
    testSet     = 'IrisTest2014.dt'
    testData = parse(testSet)
    testCollection = createCollection(testData)

    var = raw_input("Normalize? y/n\n")
    if(var == "y"):
        printAndNormalize(trainingCollection, testCollection)

    k = int(raw_input("Set max k\n"))

    if(not crossvalidate):
        bestRatio = 0
        for i in range(1,k+1):
            (curRatio, curK) = runTest(i, trainingCollection, testCollection)
            if(bestRatio <= curRatio):
                bestRatio = curRatio
                bestK = curK
        print "The best ratio was: " + str(bestRatio) + " with a k value of " + str(bestK)
    else:
        subTraining = splitList(len(trainingCollection)/numOfCuts, trainingCollection)
        res = []
        i = 0
        while(i < len(subTraining)):
            testCollection = []
            trainingCollection = []
            for test in subTraining:
                if test != subTraining[i]:
                    trainingCollection.extend(test)
            print "\nTestCase: " + str(i) + ":" 
            res.append(collect(k, trainingCollection, subTraining[i]))
            i += 1
        i = 1
        returns = [(0,0)] * (k)
        j = 1
        for test in res:
            time.sleep(0.1)
            for (k, ratio) in test:
                returns[k-1] = tuple(map(operator.add, returns[k-1], (k,ratio)))
            j += 1
        print "\n\nAverage result: "
        bestRatio = 0
        for (i, ratio) in returns:
            time.sleep(0.01)
            (curRatio, curK) = printTest(ratio/numOfCuts, i/numOfCuts,
                                         len(subTraining[0]))
                                         # len(testCollection) - len(subTraining[0]))
            if(bestRatio <= curRatio):
                bestRatio = curRatio
                bestK = curK
        print "The best ratio was: " + str(bestRatio) + " with a k value of " + str(bestK)
