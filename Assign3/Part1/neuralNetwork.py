import time

class Layer:
    name = "unnamed"
    neurons = None

    def __init__(self, name):
        self.name = name
        self.neurons = []
        self.say("Hello World!")

    def sendToLayer(self, layer):
        print ""
        self.say("sending to " + layer.getName())
        for reciever in layer.getNeurons():
            for sender in self.neurons:
                reciever.addRecieveFrom(sender)
                sender.addSendTo(reciever)

    def recieveFromLayer(self, layer):
        print ""
        self.say("recieving from " + layer.getName())
        senders = layer.getNeurons()
        for reciever in self.neurons:
            for sender in senders:
                reciever.addRecieveFrom(sender)
                sender.addSendTo(reciever)

    def addNeuron(self, neuron):
        self.say("got something named \"" + neuron.getName() + "\"")
        self.neurons.append(neuron)

    def getNeurons(self):
        return self.neurons

    def getName(self):
        return self.name

    def say(self, message):
        print self.name + ": " + message

class Neuron:

    name = "unnamed"

    value = None

    transformFunc = None

    # reciever contains the neurons this neuron send information to (does not
    # include weigh)
    sendTo = None

    # reciever contains the neurons this neuron recieves information from
    # includes weigh)
    recieveFrom = None


    def __init__(self, func, name):
        self.sendTo = []
        self.recieveFrom = []
        self.name = name
        self.transformFunc = func
        self.say("Hello world!")

    def broadcast(self, input):
        self.say("broadcasting " + str(input))
        self.value = input
        self.sendAll()

    def addRecieveFrom(self, neigh):
        self.say("got a new node named \"" + neigh.getName() + "\" listening to it!")
        self.recieveFrom.append((neigh, 1))

    def addSendTo(self, neigh):
        self.say("got a new node named \"" + neigh.getName() + "\" sending to it!")
        self.sendTo.append((neigh, 1))

    def transferFromNeuron(self, sender, x, weigh):
        self.say("got a message from \"" + sender.getName() + "\" saying " + str(x))
        self.value = self.transformFunc(x)
        self.sendAll()

    def sendAll(self):
        for (neighbor, weigh) in self.sendTo:
            neighbor.transferFromNeuron(self, self.value, weigh)

    def updateWeigh(self, x):
        # Do something to update weights
        for (neighbor, weigh) in self.recieveFrom:
            neighbor.updateWeigh(x)

    def getValue(self):
        print ""
        self.say("Im outputting: " + str(self.value))
        return self.value

    def say(self, message):
        print "    " + self.name + ": " + message

    def getName(self):
        return self.name

def addConnection(a,b):
    a.sendToLayer(b)
    b.recieveFromLayer(a)

# Transfer funcions
def nonLinear(x):
    return x/(1 + abs(x))

def linear(x):
    return x

layers = []

print "Creating Layers"
print "----------------------------------------------------------"
layers.append(Layer("Int Layer"))
layers.append(Layer("Hid Layer"))
layers.append(Layer("Out Layer"))
print "----------------------------------------------------------"
print "Done creating layers! \n"

print "Creating Nodes"
print "----------------------------------------------------------"
input = Neuron(linear, "Inp neuron")
hiden1= Neuron(nonLinear, "Hid neuron1")
# hiden2= Neuron(nonLinear, "Hid neuron2")
output = Neuron(linear, "Out neuron")
print "----------------------------------------------------------"
print "Done creating! \n"

print "Adding nodes to layers"
print "----------------------------------------------------------"
layers[0].addNeuron(input)
layers[1].addNeuron(hiden1)
# layers[1].addNeuron(hiden2)
layers[2].addNeuron(output)
print "----------------------------------------------------------"
print "Done adding! \n"

print "Adding connections between layers"
print "----------------------------------------------------------"
addConnection(layers[0], layers[1])
addConnection(layers[1], layers[2])
print "----------------------------------------------------------"
print "Done building! \n"

print "Sending!"
input.broadcast(1.0)
output.getValue()
