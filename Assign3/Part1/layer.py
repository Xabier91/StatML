import random
import math

class Layer:
    talk = False
    name = "unnamed"
    neurons = None

    # weights is a tuple of 4 elements, sender neuron, reciever neuron, weigh and last error
    weights = None
    nextLayer = None
    prevLayer = None

    learnConst = None
    mom = None

    def __init__(self, name, learnConst, momentum):
        self.mom = momentum
        self.learnConst = learnConst
        self.weights = []
        self.name = name
        self.neurons = []
        self.say("Hello World!")

    def sendToLayer(self, layer):
        self.nextLayer = layer
        layer.prevLayer = self
        self.say("sending to " + layer.getName())
        for reciever in layer.getNeurons():
            for sender in self.neurons:
                self.weights.append((sender, reciever, random.uniform(0,1), 0))
                # self.weights.append((sender, reciever, 1, 0))
                reciever.addRecieveFrom(sender)
                sender.addSendTo(reciever)

    def getErrors(self):
        errors = []
        for neuron in self.neurons:
            errors.append((neuron, neuron.getError()))
        return errors 

    def backpropogate(self, errors):
        # self.say("Im doing backpropogation. Next layer is " + str(self.nextLayer) + ". Prev layer is " + str(self.prevLayer))
        if self.nextLayer is not None:
            # self.say("I found a nextLayer: " + self.nextLayer.getName())
            errors = self.nextLayer.getErrors()
            for neuronThis in self.neurons:
                newError = 0
                for (neuronNext, error) in errors:
                    weight = self.findWeight(neuronThis, neuronNext)
                    # self.say("error of " + str(error * weight) + "to neuron " + str(neuronThis.getName())) 
                    newError += error * weight 
                neuronThis.setError(newError)
        # only used in the output layer
        else:
            for i in range(len(self.neurons)):
                self.neurons[i].setError(errors[i])
        if self.prevLayer is not None:
            self.prevLayer.backpropogate(0)
        # The only layer with no previous layer is the input layer, 
        # so when this is reached we have updated all errors and can
        # start updating weights
        else:
            self.newLine()
            self.say("Found all errors. Calculating new weights")
            self.calculateNewWeights()
            # self.say("i should be input")

    def getWeights(self, retWeights):
        for _, _, weight, _ in self.weights:
           retWeights.append(weight)
        if self.nextLayer is not None:
            return self.nextLayer.getWeights(retWeights)
        else:
            return retWeights

    def calculateNewWeights(self):
        self.newLine()
        self.say("Calculating new weights")
        for i in range(len(self.weights)):
            sender, reciever, weight, momentum = self.weights[i]
            # print reciever.getError()
            # print momentum
            newWeight = self.learnConst * reciever.getError() * self.derivativeOfLinearFunc(reciever.getValue()) * sender.getValue() + momentum * self.mom# * reciever.getValue()
            newMomentum = newWeight - weight
            # print "changed weight with " + str(delta)
            # newWeight = delta #weight + delta
            self.say("Calculated new weigh between " + sender.getName() + " and " + reciever.getName() + ". Old was " + str(weight) + ". New is " + str(newWeight))
            # print ("Calculated new weigh between " + sender.getName() + " and " + reciever.getName() + ". Old was " + str(weight) + ". New is " + str(newWeight))
            self.weights[i] = (sender, reciever, newWeight, newMomentum)
        if self.nextLayer is not None:
            self.nextLayer.calculateNewWeights()
        else:
            self.say("Im output layer, ready for new run")

    def derivativeOfLinearFunc(self, x):
        return 1/(math.pow((1 + abs(x)),2))

    def findWeight(self, sender1, reciever1):
        for (sender2, reciever2, weight, _) in self.weights:
            if sender2 == sender1 and reciever1 == reciever2:
                return weight
        return 0

    def calculate(self):
        self.newLine()
        self.say("Asking my layer to calculate and send")
        for neuron in self.neurons:
            neuron.calculateAndSend()

        if self.nextLayer is not None:
            self.newLine()
            self.say("Sending weights to next layer")
            for (sender, reciever, weigh, _) in self.weights: 
                reciever.recieveWeigh(sender, weigh)     
            self.nextLayer.calculate()
        

    def addNeuron(self, neuron):
        self.say("got something named \"" + neuron.getName() + "\"")
        self.neurons.append(neuron)

    def getNeurons(self):
        return self.neurons

    def getName(self):
        return self.name

    def say(self, message):
        if self.talk:
            print self.name + ": " + message

    def newLine(self):
        if self.talk:
            print "\n"
