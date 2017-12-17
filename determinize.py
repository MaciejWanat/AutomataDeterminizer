#!/usr/bin/env python3

import sys
import collections

determineAutomaton = {}
automaton = {}
acceptStates = []
alphabet = set()
foundState = True

def prettyPrint(dicto):
    print()
    for key in dicto:
        print(str(key) + " : " + str(dicto[key]))

def prettyPrintOrdered(dicto):
    print()
    dicto = collections.OrderedDict(sorted(dicto.items()))
    for key in dicto:
        print(str(key) + " : " + str(dicto[key]))

#Read nondeterministic automaton ----
for line in sys.stdin:
	if line[0] != '#':
		words = line.strip().split(' ')
		if len(words) != 1:
			pair = (words[0], words[2])
			alphabet.add(words[2])
			if pair in automaton:
				automaton[pair].add(words[1])
			else:
				automaton[pair] = set(words[1])
		else:
			acceptStates.append(line.strip())

determineAutomaton = dict(automaton)
i = 0
#Determine into multistates----
#while you can find any unmapped multistate
while foundState == True:
    i = i + 1
    print('----------------')
    print('Iteration ' + str(i))
    prettyPrint(determineAutomaton)
    print()
    #iterate through 'automaton', add new states to 'determineAutomaton'.
    #if you add anything, check if there is any new unmapped state.
    foundState = False
    automaton = dict(determineAutomaton)
    #for each state-symbol pair...
    for key in automaton:
        #check if it is a multistate (can get more than one state), and if it is
        if len(automaton[key]) > 1 and (frozenset(automaton[key]), key[-1]) not in automaton:

            print('Found multistate : ' + str(automaton[key]) + ". Adding to automaton...")
            foundState = True
            #for each symbol in alphabet...
            for symbol in alphabet:
                valueAutoma = set()
                #for each state in multstational state...
                for state in automaton[key]:
                    #add states you can get to from single state and current symbol, if the connection exists
                    if (state, symbol) in automaton:
                        valueAutoma.update(automaton[(state, symbol)])

                keyAutoma = (frozenset(automaton[key]), symbol)
                determineAutomaton[keyAutoma] = valueAutoma

#Delete no longer needed single states
for key in automaton:
    if type(key[0]) is str and key[0] != '0':
        del determineAutomaton[key]

automaton = determineAutomaton
#Multistates into determine values
#Set int value for every state and map it

#Create map
keysMap = {}
#Map multistates and 0 to 0
keysMap['0'] = '0'
i = 1
for key in determineAutomaton:
    if key[0] not in keysMap:
        keysMap[key[0]] = str(i)
        i = i + 1

print("--------\nMap:")
prettyPrint(keysMap)
print()

determineAutomaton = {}
#Map values
for key in automaton:
    #transfer value set into frozenset, if it is a set or into single element if it is a single element
    if len(automaton[key]) > 1:
        determineAutomaton[(keysMap[key[0]], key[1])] = keysMap[frozenset(automaton[key])]
    else:
        for e in automaton[key]:
            singleElement = e
        determineAutomaton[(keysMap[key[0]], key[1])] = keysMap[singleElement]

print("Final automaton:")
prettyPrintOrdered(determineAutomaton)
