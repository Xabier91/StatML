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

ttest = extractT(testData)
ttrain = extractT(trainData)
actual = ttest

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



def findMeans(data):
    ret = []
    for row in data:
        ret.append(np.mean(row))
    return ret

# Basic functions

def w0(phimean, ws):
    """ttest is the target vector"""
    # print ws
    # print retval
    sum = np.mean(ttest) - np.sum(ws * phimean)
    return sum

def transpose(data):
    transposed = []
    for column in range(len(data[0])):
        transposed.append([])
    for row in range(len(data)):
        for column in range(len(data[row])):
            transposed[column].append(data[row][column])
    return transposed

def maxLikelyhoodbias(xs,ws, w0):
    xs = np.array(xs)
    ws = np.array(ws)
    ret = []
    bias = []

    weigthphi = []

    xs = transpose(xs)
    for i in range(len(xs)):
        retval = 0 + w0 
        for weigth in range(len(ws)):
            retval += xs[i][weigth] * ws[weigth]
        ret.append(retval)
    return ret

def maxLikelyhood(xs,ws):
    xs = np.array(xs)
    ws = np.array(ws)
    ret = []
    bias = []

    weigthphi = []

    #find biases
    for column in range(len(xs)):
        weigthphi.append(sum(xs[column])/len(xs[column]) * ws[column])
    bias = sum(ttest)/len(ttest) - sum(weigthphi)

    xs = transpose(xs)
    for i in range(len(xs)):
        retval = 0 + bias
        for weigth in range(len(ws)):
            retval += xs[i][weigth] * ws[weigth]
        ret.append(retval)
    return ret

def MAP(trainset, testset, rmsold, wML):
  
    designMatrix = np.matrix(patsy.dmatrix(trainset)) #np.array(patsy.dmatrix(train2))[0]
    plotVals = []
    plotAlphas = []

    bestmN = 0
    bestrms = float("inf")
    bestNum = 0

    for num in drange(0, 7.0, 0.001):
        alpha = pow(10, num)

        SN = alpha * np.identity(len(designMatrix)) + designMatrix * designMatrix.T

        mN = np.linalg.inv(SN) * designMatrix * np.matrix(ttrain)

        predicted = maxLikelyhood(testset, mN)
        rms = math.sqrt(skm.mean_squared_error(ttest, predicted))
        if(rms < bestrms):
            bestrms = rms
            bestmN = mN
            bestNum = num
        plotVals = np.append(plotVals, rms)
        plotAlphas = np.append(plotAlphas, num)

    print "bestmN = " + str(bestmN)
    print "bestrms = " + str(bestrms)
    print "bestAlpha = " + str(bestNum)

    plt.plot(plotAlphas, np.repeat(rmsold,len(plotVals)), "b-", label = "Using MLS")
    plt.plot(plotAlphas, plotVals, "r-", label = "Using MAP")
    plt.show()

# Extracting data
test1 = extract1(testData).T
test2 = extract2(testData).T
test3 = extract3(testData).T

train1 = extract1(trainData).T
train2 = extract2(trainData).T
train3 = extract3(trainData).T

# Calculating
wML1 = sum(np.linalg.pinv(np.array(train1)) * ttrain)
wML2 = sum(np.linalg.pinv(np.array(train2)) * ttrain)
wML3 = sum(np.linalg.pinv(np.array(train3)) * ttrain)


# Plotting
# predicted = maxLikelyhood(test1, wML1)
# plt.plot(actual, "ro", label = "data")
# plt.plot(predicted, "b-", label = "fit")
# rms1 = math.sqrt(skm.mean_squared_error(actual, predicted))
# print "Selection 1 rms = " + str(rms1)
# plt.show()

predicted = maxLikelyhood(test2, wML2)
plt.plot(ttest, "ro", label = "data")
plt.plot(predicted, "b-", label = "fit")
rms2 = math.sqrt(skm.mean_squared_error(actual, predicted))
print "Selection 2 rms = " + str(rms2)
plt.show()


plt.plot(train2, ttrain.T, "bo")
plt.plot(predicted, ttest, "ro")
# plt.plot([0,200], [0,200])
plt.show()

# predicted = maxLikelyhood(test3, wML3)
# plt.plot(ttest, "ro", label = "data")
# plt.plot(predicted, "b-", label = "fit")
# rms3 = math.sqrt(skm.mean_squared_error(actual, predicted))
# print "Selection 3 rms = " + str(rms3)
# plt.show()

# MAP(train1, test1, rms1, wML1)
# MAP(train2, test2, rms2, wML2)
# MAP(train3, test3, rms3, wML3)


