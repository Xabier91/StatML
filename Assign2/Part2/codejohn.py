import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import scipy.stats as norm
import time
import math
import sklearn.metrics as skm
import patsy
# from sklearn.metrics import mean_squared_error

trainData = "sunspotsTrainStatML.dt"
testData = "sunspotsTestStatML.dt"

def drange(start, stop, step):
         r = start
         while r < stop:
                 yield r
                 r += step

def extract1(filePath):
    extraction = []
    for line in parse(filePath):
       extraction.append([float(line[2]), float(line[3])])
    return np.array(extraction)

def extract2(filePath):
    extraction = []
    for line in parse(filePath):
       extraction.append([float(line[4])])
    return np.array(extraction)

def extract3(filePath):
    extraction = []
    for line in parse(filePath):
        extraction.append([float(x) for x in line[0:5]])
    return np.array(extraction)

def extractT(filePath):
    extraction = []
    for line in parse(filePath):
        extraction.append([float(line[5])])
    return np.array(extraction)

def parse(filePath):
    ret = []
    f = open(filePath, 'r')
    for line in f.read().split('\n'):
        ret.append(line.split(' '))
    del ret[-1]
    return ret

def findMeans(data):
    ret = []
    for row in data:
        ret.append(np.mean(row))
    return ret

# Basic functions

def w0(t, retval, ws):
    return np.mean(t) - np.sum(ws * retval)

def maxLikelyhood(xs,ws):
    ws = np.array(ws)
    ret = []
    for i in range(len(xs[0])):
        retval = 0
        for j in range(len(xs)):
            retval += xs[j][i] * ws[j][0]
        # retval += w0(t, zip(*xs)[i], ws)  I dont know why this does not work
        ret.append(retval)
    return ret

def identityBasic(input):
    return input

def gaussianBasic(input):
    return np.exp(-(input - np.mean(input)/(np.power(2*np.std(input),2))))



# Extracting data
test1 = extract1(testData).T
test2 = extract2(testData).T
test3 = extract3(testData).T
ttest = extractT(testData)

train1 = extract1(trainData).T
train2 = extract2(trainData).T
train3 = extract3(trainData).T
ttrain = extractT(trainData)

# Calculating
wML1 = np.array(np.linalg.pinv(np.matrix(findMeans(train1))) * np.mean(ttrain))
wML2 = np.array(np.linalg.pinv(np.matrix(findMeans(train2))) * np.mean(ttrain))
wML3 = np.array(np.linalg.pinv(np.matrix(findMeans(train3))) * np.mean(ttrain))


actual = ttest
# Plotting
predicted = maxLikelyhood(test1, wML1)
plt.plot(actual, "ro", label = "data")
plt.plot(predicted, "b-", label = "fit")
rms1 = math.sqrt(skm.mean_squared_error(actual, predicted))
print "Selection 1 rms = " + str(rms1)
plt.show()

predicted = maxLikelyhood(test2, wML2)
plt.plot(ttest, "ro", label = "data")
plt.plot(predicted, "b-", label = "fit")
rms2 = math.sqrt(skm.mean_squared_error(actual, predicted))
print "Selection 2 rms = " + str(rms2)
plt.show()

predicted = maxLikelyhood(test3, wML3)
plt.plot(ttest, "ro", label = "data")
plt.plot(predicted, "b-", label = "fit")
rms3 = math.sqrt(skm.mean_squared_error(actual, predicted))
print "Selection 3 rms = " + str(rms3)
plt.show()

actual = ttrain
designMatrix = np.matrix(patsy.dmatrix(train3))
plotVals = []

for num in drange(1, 10.0, 0.2):
    alpha = pow(10, num)
    # S0 = pow(alpha,-1) * np.identity(len(designMatrix))

    SN = pow(alpha * np.identity(len(designMatrix)) + designMatrix * designMatrix.T, -1)
    mN = SN * designMatrix * actual

    predicted = maxLikelyhood(train3, mN)
    rms = math.sqrt(skm.mean_squared_error(actual, predicted))
    plotVals = np.append(plotVals, rms)


plt.plot(np.repeat(rms3, len(plotVals)), "b-")
plt.plot(plotVals, "r-")
plt.show()
