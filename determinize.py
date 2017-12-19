#!/usr/bin/env python3

import sys
import collections

detAutomaton = {}
nonDetAutomaton = {}
acceptStates = set()
detAcceptStates = set()
alphabet = set()
foundState = True
nonDetWalks = False

def prettyPrint(dicto):
    print()
    for key in dicto:
        print(str(key) + " : " + str(dicto[key]))

def prettyPrintOrdered(dicto, acceptStates):
    print()
    dicto = collections.OrderedDict(sorted(dicto.items()))
    for key in dicto:
        print(str(key[0]) + " " + str(dicto[key]) + " " + str(key[1]))
    for state in acceptStates:
    	print(state)

def printIter(dicto, i):
	print('\n----------------\n')
	print('Iteration ' + str(i))
	prettyPrint(dicto)
	print()

#Read nondeterministic automaton ----
for line in sys.stdin:
	if line[0] != '#':
		words = line.strip().split(' ')
		if len(words) != 1:
			pair = (words[0], words[2])
			alphabet.add(words[2])
			if pair in nonDetAutomaton:
				nonDetAutomaton[pair].add(words[1])
				#used for detecting not needed single states
				nonDetWalks = True
			else:
				nonDetAutomaton[pair] = set(words[1])
		else:
			acceptStates.add(line.strip())

detAcceptStates = set(acceptStates)

print('Input: ')
prettyPrint(nonDetAutomaton)

#if the input automaton is nondeterministic
if nonDetWalks:

	#initialize values for 0
	for symbol in alphabet:
		if ('0', symbol) in nonDetAutomaton:
			detAutomaton[('0', symbol)] = nonDetAutomaton[('0', symbol)] 

	#used because we cant iterate throught changing dictionary
	detAutomatonCopy = dict(detAutomaton)
	i = 0

	while foundState == True:
		detAutomaton = dict(detAutomatonCopy)

		i = i + 1
		printIter(detAutomaton, i)

		foundState = False

		for key in detAutomaton:
			compareKey = key			
			#if its a set, convert it into frozenset (which is hashable)	
			if len(detAutomaton[key]) > 1:
				compareKey = (frozenset(detAutomaton[key]),key[-1])
			elif detAutomaton[key]:
				compareKey = (next(iter(detAutomaton[key])), key[-1])				

			if detAutomaton[key] and compareKey not in detAutomaton:

				print('Found new key : ' + str(detAutomaton[key]) + ". Adding to automaton...")
				foundState = True

				for symbol in alphabet:
					valueAutoma = set()
					for state in detAutomaton[key]:						
						if (state, symbol) in nonDetAutomaton:
							valueAutoma.update(nonDetAutomaton[(state, symbol)])	
						detAutomatonCopy[compareKey[0], symbol] = valueAutoma

	#Delete empty states
	toDel = set()

	for key in detAutomaton:
		if not len(detAutomaton[key]):
			toDel.add(key)

	for state in toDel:
		del detAutomaton[state]

	i = i + 1
	printIter(detAutomaton, i)

	#Create map
	keysMap = {}

	#Map starting state
	keysMap['0'] = '0'

	i = 1
	#Map lasting states
	for key in detAutomaton:
	    if key[0] not in keysMap:
	        keysMap[key[0]] = str(i)
	        i = i + 1

	print("--------\n\nMap:")
	prettyPrint(keysMap)
	print()        

	detAcceptStates = set()

	#Get accepting states
	for key in detAutomaton:
		for state in frozenset(key[0]):
			if state in acceptStates:
				detAcceptStates.add(keysMap[key[0]])

	detAutomatonCopy = detAutomaton
	detAutomaton = {}

	#Map values
	for key in detAutomatonCopy:
	    #transfer value set into frozenset, if it is a set or into single element if it is a single element
	    if len(detAutomatonCopy[key]) > 1:
	        detAutomaton[(keysMap[key[0]], key[1])] = keysMap[frozenset(detAutomatonCopy[key])]
	    else:
	        for e in detAutomatonCopy[key]:
	            singleElement = e
	        detAutomaton[(keysMap[key[0]], key[1])] = keysMap[singleElement]
	
	print("--------\n\nFinal deterministic automaton:")
	prettyPrintOrdered(detAutomaton, detAcceptStates)

else:	
	print("\nYour automaton is already deterministic!")