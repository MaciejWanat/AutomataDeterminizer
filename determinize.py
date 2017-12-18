#!/usr/bin/env python3

import sys
import collections

determineAutomaton = {}
automaton = {}
acceptStates = set()
detAcceptStates = set()
alphabet = set()
foundState = True
nonDetWalks = set()

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

#Read nondeterministic automaton ----
for line in sys.stdin:
	if line[0] != '#':
		words = line.strip().split(' ')
		if len(words) != 1:
			pair = (words[0], words[2])
			alphabet.add(words[2])
			if pair in automaton:
				automaton[pair].add(words[1])
				#used for detecting not needed single states
				nonDetWalks.add(int(words[0]))
			else:
				automaton[pair] = set(words[1])
		else:
			acceptStates.add(line.strip())

determineAutomaton = dict(automaton)
detAcceptStates = set(acceptStates)

#if the input automaton is nondeterministic
if len(nonDetWalks):
	maxDet = min(nonDetWalks)	
	i = 0
	#Determine into multistates----
	#while you can find any unmapped multistate
	while foundState == True:
	    i = i + 1
	    print('----------------')
	    print('Iteration ' + str(i))
	    prettyPrint(determineAutomaton)
	    print()
	    #iterate through 'automaton' and add new states to 'determineAutomaton'.
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
		if isinstance(key[0], str) and len(determineAutomaton[key]) == 1 and int(key[0]) > maxDet:
			del determineAutomaton[key]

	automaton = determineAutomaton
	orderedSingleAutomaton = {}

	#Create map
	i = 0
	keysMap = {}

	#Map single states
	while i <= maxDet:
		keysMap[str(i)] = str(i)
		i = i + 1

	#Map multistates
	for key in determineAutomaton:
	    if key[0] not in keysMap:
	        keysMap[key[0]] = str(i)
	        i = i + 1

	print("--------\nMap:")
	prettyPrint(keysMap)
	print()

	detAcceptStates = set()
	#Get accepting states
	for key in automaton:
		if isinstance(key[0], frozenset):
			for state in key[0]:
				if state in acceptStates:
					detAcceptStates.add(keysMap[key[0]])

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
	
print("Final deterministic automaton:")
prettyPrint(determineAutomaton)
prettyPrintOrdered(determineAutomaton, detAcceptStates)