# coding=utf-8
# Author: Henry Bergström, 920924-3113
# Description: Enigma (3-rot, 3-plug) Function library
# Date: 2016-12-04


class Reflector(object):

   def __init__(self, rotor):
       self.rotor = rotor

   def getRotor(self):
       return self.rotor

   def getOutput(self,inp):
       return self.rotor[inp]

   def setRotor(self,rotor):
       self.rotor = rotor

#######################################

class Rotor(Reflector):
    def __init__(self, rotor, rotorNr, name):
        Reflector.__init__(self, rotor)
        self.rotorNr = rotorNr
        self.rotationCounter = 0
        self.name = name

    def getName(self):
        return self.name

    def rotate(self, n):
        self.rotor[:] = self.rotor[n:] + self.rotor[:n]

    def getRotorNr(self):
        return self.rotorNr

    def setRotorNr(self,nr):
        self.rotorNr = nr

    def getRotationCount(self):
        return self.rotationCounter

    def incrementRotationCounter(self):
        self.rotationCounter += 1

    def getInvOutput(self, inp):
       return self.rotor.index(inp)

######################################

class PlugCable(object):
    def __init__(self, cable):
        self.cable = cable

    def trySwap(self,inp):
        if self.cable[0] == inp:
            return self.cable[1]
        elif self.cable[1] == inp:
            return self.cable[0]
        else:
            return inp

    def getCableChar(self):
        return [chr(self.cable[0]+97), chr(self.cable[1]+97)]

    def getCable(self):
        return [self.cable[0], self.cable[1]]

####################################

## CONSTANT VALUES ##
alphabet = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
rotor1 = Rotor([8, 19, 0, 20, 4, 22, 25, 12, 16, 21, 3, 1, 13, 2, 5, 15, 11, 24, 18, 23, 6, 10, 14, 9, 17, 7], 0, "rotor1")
rotor2 = Rotor([17, 25, 16, 19, 1, 11, 3, 15, 22, 18, 10, 9, 13, 0, 5, 2, 14, 12, 20, 21, 6, 4, 23, 24, 8, 7], 1, "rotor2")
rotor3 = Rotor([24, 23, 5, 22, 0, 6, 1, 10, 17, 8, 13, 9, 3, 12, 14, 21, 15, 20, 4, 18, 11, 7, 25, 16, 2, 19], 2, "rotor3")
rotors = [rotor1,rotor2,rotor3]
reflector = Reflector([14, 15, 13, 16, 18, 17, 21, 20, 19, 25, 24, 23, 22, 2, 0, 1, 3, 5, 4, 8, 7, 6, 12, 11, 10, 9])

########################
class Enigma(object):
    def __init__(self,plugCables, rotors, reflector,key):
        self.rotors = {}
        self.plugCables = {}
        self.plugCables = plugCables
        self.rotors = rotors
        self.reflector = reflector 
        self.rotationCounter = 0
        self.key = key
        self.setKeyConfig()

    def setPlugCables(self, pcs):               # creates 3 plugcables from int array 0-5
        self.plugCables[0] = PlugCable([pcs[0], pcs[1]])
        self.plugCables[1] = PlugCable([pcs[2], pcs[3]])
        self.plugCables[2] = PlugCable([pcs[4], pcs[5]])

    def setRotorConfig(self, rotorComb):        # make rotor[0] the first in line and so on..
        self.rotors = rotorComb
        for i,rotor in enumerate(self.rotors):
            self.rotors[i].setRotorNr(i)

    def setKeyConfig(self):                 # rotate rotors until key is at index 0
        for i in range(0,3):
            while True:
                if self.rotors[i].rotor[0] == self.key[i]:
                    break
                self.rotors[i].rotate(1)

    def getPlugCables(self):
        return [self.plugCables[0].getCable(), self.plugCables[1].getCable(), self.plugCables[2].getCable()]

    def getRotorNames(self):
        retArr = ['x'] * len(rotors)
        for i,val in enumerate(self.rotors):
            retArr[i] = self.rotors[i].getName()
        return retArr

## Rotate rotors
    def adjustRotation(self):
        for i in range(0,3):
            rotateFlag = self.rotationCounter % pow(26,self.rotors[i].getRotorNr())
            if rotateFlag == 0:
                self.rotationCounter += 1
                self.rotors[i].rotate(1)
                self.rotors[i].incrementRotationCounter()

## Remove any spaces or special signs
    def removeExtras(self, input):
        temp = input.translate(None, '!@#$" "')
        temp.replace(" ", "")
        return temp.lower()

## Encryption
    def encrypt(self, messageString):
        self.setKeyConfig()                   # reset rotors to key            
        self.rotationCounter = 0

                
        # if cmp(self.key, [0,1,3]) == 0:
        #     printSuccesfulSettings(self)

        messageString = self.removeExtras(messageString)
        messageList = (list(messageString))     ## make message to string array
        encrypted = ""
        for c in (messageList):                 ## Loop through array
            c = ord(c) - 97                     ## From letters to numbers: a = 0, b = 1
            for j in range(0,3):
                c = self.plugCables[j].trySwap(c) ## if c is connect to any of the PlugCables
            c = self.rotors[0].getOutput(c)             ## go through rotors
            self.adjustRotation()                       ## rotate rotors
            c = self.rotors[1].getOutput(c)
            self.adjustRotation()                       ## rotate rotors
            c = self.rotors[2].getOutput(c)
            self.adjustRotation()                       ## rotate rotors
            c = self.reflector.getOutput(c)
            self.adjustRotation()                       ## rotate rotors
            c = self.rotors[2].getInvOutput(c)
            self.adjustRotation()                       ## rotate rotors
            c = self.rotors[1].getInvOutput(c)
            self.adjustRotation()                       ## rotate rotors
            c = self.rotors[0].getInvOutput(c)
            self.adjustRotation()                       ## rotate rotors
            for k in range(2, -1, -1):                        ## check cables again
                c = self.plugCables[k].trySwap(c)
            c = c + 97

            encrypted += chr(c)
        return encrypted

##################################################
#HELP FUNCTIONS#
##################################################
import random
import string
def makeKeyChar(key):       #
    charArr = ['X'] * 3
    for i,val in enumerate(key):
        charArr[i] = chr(val+97)
    return ''.join(charArr)

def printSuccesfulSettings(anEnigma):
    print "PlugCables:", anEnigma.getPlugCables()
    print "Rotors position:", anEnigma.getRotorNames()
    print "rotor1:", [chr(i+97) for i in anEnigma.rotors[0].getRotor()]
    print "rotor2:", [chr(i+97) for i in anEnigma.rotors[1].getRotor()]
    print "rotor3:", [chr(i+97) for i in anEnigma.rotors[2].getRotor()]
    print "Key:", makeKeyChar(anEnigma.key)

def getRandomSampleFromAlpha(alphabet, n):
       return random.sample(alphabet, n)

def makePlugCablesfromSample(sample):
    pcArr = [None] * 3
    pcArr[0] = PlugCable([sample[0],sample[1]])
    pcArr[1] = PlugCable([sample[2],sample[3]])
    pcArr[2] = PlugCable([sample[4],sample[5]])
    return pcArr

