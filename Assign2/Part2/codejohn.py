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
# wML1 = np.array(np.linalg.pinv(np.matrix(findMeans(train1))) * np.mean(ttrain))
# wML2 = np.array(np.linalg.pinv(np.matrix(findMeans(train2))) * np.mean(ttrain))
wML3 = np.array(np.linalg.pinv(np.matrix(findMeans(train3))) * np.mean(ttrain))


actual = ttest
# Plotting
# predicted = maxLikelyhood(test1, wML1)
# plt.plot(actual, "ro", label = "data")
# plt.plot(predicted, "b-", label = "fit")
# rms = math.sqrt(skm.mean_squared_error(actual, predicted))
# print rms
# plt.show()

# predicted = maxLikelyhood(test2, wML2)
# plt.plot(ttest, "ro", label = "data")
# plt.plot(predicted, "b-", label = "fit")
# rms = math.sqrt(skm.mean_squared_error(actual, predicted))
# print rms
# plt.show()

predicted = maxLikelyhood(test3, wML3)
plt.plot(ttest, "ro", label = "data")
plt.plot(predicted, "b-", label = "fit")
rmsb = math.sqrt(skm.mean_squared_error(actual, predicted))
# print rms
plt.show()

plotVals = np.array([]) 
alphas = np.array([]) 
bestalpha = 0
bestMN = 0

actual = ttrain
designMatrix = np.matrix(patsy.dmatrix(train3))
m0 = 0

for num in drange(1, 10.0, 0.2):
# for alpha in drange(-640765.0, -640764.0,0.02):
    alpha = pow(10, num)
    S0 = pow(alpha,-1) * np.identity(len(designMatrix))

    # print len(designMatrix.T * designMatrix)
    # print len(designMatrix)
    SN = pow(alpha * np.identity(len(designMatrix)) + designMatrix * designMatrix.T, -1)
    # print "SN has dimensions: (" + str(len(SN)) + ", " + str(len(SN[0])) + ")"
    mN = SN * designMatrix * actual
    # print "mN has dimensions: (" + str(len(mN)) + ", " + str(len(mN[0])) + ")"
    # print "for alpha = " + str(alpha) + " the range is " + str(mN)
    # plotVals = np.append(plotVals, mN)
    # if (mN > bestMN):
        # bestalpha, bestMN = alpha, mN
    # bestalpha = max(alpha 
    # print mN
    # print plotVals
    # print mN
    # print np.sum(mN)
    predicted = maxLikelyhood(train3, mN)
    rms = math.sqrt(skm.mean_squared_error(actual, predicted))
    plotVals = np.append(plotVals, rms)
    # print rms
    # plt.plot(ttrain, "ro", label = "data")
    # plt.plot(predicted)
    # plt.show()


# print bestalpha, bestMN
print plotVals
plt.plot( np.repeat(rmsb, len(plotVals)), "b-")
plt.plot(plotVals, "r-")
plt.show()
