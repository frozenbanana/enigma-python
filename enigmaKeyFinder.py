# coding=utf-8
import enigmaLib
import random
import itertools

# Enigma configuration
rotor1 = enigmaLib.Rotor([8, 19, 0, 20, 4, 22, 25, 12, 16, 21, 3, 1, 13, 2, 5, 15, 11, 24, 18, 23, 6, 10, 14, 9, 17, 7], 0, "rotor1")
rotor2 = enigmaLib.Rotor([17, 25, 16, 19, 1, 11, 3, 15, 22, 18, 10, 9, 13, 0, 5, 2, 14, 12, 20, 21, 6, 4, 23, 24, 8, 7], 1, "rotor2")
rotor3 = enigmaLib.Rotor([24, 23, 5, 22, 0, 6, 1, 10, 17, 8, 13, 9, 3, 12, 14, 21, 15, 20, 4, 18, 11, 7, 25, 16, 2, 19], 2, "rotor3")
rotors = [rotor1,rotor2,rotor3]
reflector = enigmaLib.Reflector([14, 15, 13, 16, 18, 17, 21, 20, 19, 25, 24, 23, 22, 2, 0, 1, 3, 5, 4, 8, 7, 6, 12, 11, 10, 9])

amountSolutions = 1 
initPlugArray = enigmaLib.makePlugCablesfromSample([0,1,2,3,4,5])
initKey = [0,0,0] #aaa
iterEnigma = enigmaLib.Enigma(initPlugArray, rotors, reflector, initKey)

print "Welcome to Henrys plain text attack program specialized for the Enigma machine (3 rotors)"
clText = raw_input("Enter clear text: \n")
enText = raw_input("Enter encrypted text: \n")

print "-------------------"
print "A clear text:", clText
print "should give the crypto text:", enText
print "This program will find",amountSolutions,"possible solutions for a 3-plugcabled Enigma with 3 known rotors"
enigmaLib.printSuccesfulSettings(iterEnigma)
solution = 0

raw_input("Press enter to start key finding... (This can take a while)")

for rotorPerm in itertools.permutations(enigmaLib.rotors,3):     # Loop through every rotor config
    iterEnigma.setRotorConfig(rotorPerm)
    for pcComb in itertools.combinations(enigmaLib.alphabet, 6): # Loop through every
        iterEnigma.setPlugCables(pcComb)
        for keyComb in itertools.combinations_with_replacement(enigmaLib.alphabet, 3):      # Loop through every key
                iterEnigma.key = list(keyComb)
                if iterEnigma.encrypt(clText) == enText:                                    # Show the solutions
                    print "------------- SOLUTION", solution+1,"----------"
                    print "Current settings gave same encrypted text:", enText
                    enigmaLib.printSuccesfulSettings(iterEnigma)
                    solution +=1
                    print "-----------------------------------"
                if solution == amountSolutions:                                              # Stopping search when sufficient amount of solutions
                    break
        else:
            continue
        break
    else:
        continue
    break
