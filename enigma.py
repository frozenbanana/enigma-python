# coding=utf-8
import enigmaLib
import random

# Config for Enigma (needs to be the same in engimaKeyFinder.py)
rotor1 = enigmaLib.Rotor([8, 19, 0, 20, 4, 22, 25, 12, 16, 21, 3, 1, 13, 2, 5, 15, 11, 24, 18, 23, 6, 10, 14, 9, 17, 7], 0, "rotor1")
rotor2 = enigmaLib.Rotor([17, 25, 16, 19, 1, 11, 3, 15, 22, 18, 10, 9, 13, 0, 5, 2, 14, 12, 20, 21, 6, 4, 23, 24, 8, 7], 1, "rotor2")
rotor3 = enigmaLib.Rotor([24, 23, 5, 22, 0, 6, 1, 10, 17, 8, 13, 9, 3, 12, 14, 21, 15, 20, 4, 18, 11, 7, 25, 16, 2, 19], 2, "rotor3")
rotors = [rotor1,rotor2,rotor3]
reflector = enigmaLib.Reflector([14, 15, 13, 16, 18, 17, 21, 20, 19, 25, 24, 23, 22, 2, 0, 1, 3, 5, 4, 8, 7, 6, 12, 11, 10, 9])

## CLEAR TEXT TO BE ENCRYPTED ##
clText = raw_input("Enter text to be encrypted: \n")
ansPlug = raw_input("Set plugcables. Example - ab cd ef: \n")
ansPlug = ''.join(ansPlug.split())
plugArray = [ord(i)-97 for i in ansPlug]
plugArray = enigmaLib.makePlugCablesfromSample(plugArray)
ansKey = raw_input("Set key. Example - abc: \n")
keyArray = [ord(i)-97 for i in ansKey]

## INIT OF MACHINE ##
myEnig = enigmaLib.Enigma(plugArray, rotors, reflector, keyArray)

## PRESENT ##
print "=========================="
enigmaLib.printSuccesfulSettings(myEnig)
print "=========================="
print "Output:",clText, "->", myEnig.encrypt(clText)             # Remove to see result with random configuration
print "=========================="
