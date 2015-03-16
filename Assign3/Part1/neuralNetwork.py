from time import sleep
from sklearn.metrics import mean_squared_error
from math import sqrt
from parser import fromFile

import numpy as np
import neuron as ne
import layer as la


# Helper functions
def addConnection(a,b):
    a.sendToLayer(b)

def meanSquareError(target, actual):
    return ((target - actual) ** 2)#.mean(axis=ax)

def say(message):
    if networkTalk:
        print message

# Transfer funcions
def nonLinear(x):
    return x/(1 + abs(x))

def linear(x):
    return x


# Network API
def createNetwork(learnConst, momentum):
    ne.Neuron.talk = networkTalk
    la.Layer.talk = networkTalk
    say("Creating Layers")
    say("----------------------------------------------------------")
    layers.append(la.Layer("Int Layer", learnConst, momentum))
    layers.append(la.Layer("Hid Layer1", learnConst, momentum))
    # layers.append(la.Layer("Hid Layer2", learnConst))
    layers.append(la.Layer("Out Layer", learnConst, momentum))
    say("----------------------------------------------------------")
    say("Done creating layers! \n")

    say("Adding nodes to layers")
    say("----------------------------------------------------------")
    layers[0].addNeuron(ne.Neuron(linear, "Inp neuron"))
    layers[1].addNeuron(ne.Neuron(nonLinear, "Hid neuron11"))
    # layers[1].addNeuron(ne.Neuron(nonLinear, "Hid neuron12"))
    # layers[2].addNeuron(ne.Neuron(nonLinear, "Hid neuron21"))
    # layers[2].addNeuron(ne.Neuron(nonLinear, "Hid neuron22"))
    # layers[2].addNeuron(ne.Neuron(nonLinear, "Hid neuron23"))
    # layers[2].addNeuron(ne.Neuron(nonLinear, "Hid neuron24"))
    # layers[2].addNeuron(ne.Neuron(nonLinear, "Hid neuron25"))
    # layers[2].addNeuron(ne.Neuron(nonLinear, "Hid neuron26"))
    layers[2].addNeuron(ne.Neuron(linear, "Out neuron"))
    say("----------------------------------------------------------")
    say("Done adding! \n")

    say("Adding connections between layers")
    say("----------------------------------------------------------")
    addConnection(layers[0], layers[1])
    addConnection(layers[1], layers[2])
    # addConnection(layers[2], layers[3])
    say("----------------------------------------------------------")
    say("Done building! \n")
    return (layers[0], layers[2])

def broadcast(value, inputNeuron, outputNeuron):
    say("Broadcasting " + str(value))
    inputNeuron.broadcast(value)
    return outputNeuron.getValue() 

# debugging
layers = []
networkTalk = False
# networkTalk = True

# Network constants
learnConst = 0.010
momentum = 1.0


inputLayer, outputLayer= createNetwork(learnConst, momentum)

print "Training!"

training = fromFile("sincTrain25.dt")
for i in range(len(training)):
    (input, targetOut) = training[i]
    inputLayer.getNeurons()[0].setValue(input)
    error = 0
    j = 0
    for j in range(10):
    # for _ in range(1000):
        inputLayer.calculate()
        error = meanSquareError(outputLayer.getNeurons()[0].getValue(), targetOut)
        # print "\n\n"
        # print "Doing backpropagation!"
        # print "Finding errors!"
        outputLayer.backpropogate([error])
        # print "In -> " + str(input)
        # print "Out -> " + str(outputLayer.getNeurons()[0].getValue())# + " target was: " + str(targetOut)
        # print "Training set " + str(i) + ". Run " + str(j) + ": Error was " + str(error)
        j += 1
        # sleep(1)
    # errors.append(error)
    # actualOut = broadcast(input, inputNeuron, outputNeuron)
    # error = meanSquareError(targetOut, actualOut)  

print "Training done!"
print "Printing weights: "
print inputLayer.getWeights([])
print "Mathword mathword partial derivative numerically estimated mathword mathword"


print "Testing!"

test = fromFile("sincValidate10.dt")

errors = []
for i in range(len(test)):
    (input, targetOut) = test[i]
    inputLayer.calculate()
    error = meanSquareError(outputLayer.getNeurons()[0].getValue(), targetOut)
    errors.append(error)

print "Average error is: " + str(sum(errors)/len(errors))
