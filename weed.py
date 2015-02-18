# Imports stuff
from __future__ import division
from random import shuffle
import math
import os
from easygui import *
import sys

#------------------Game settings------------------
# Humans ammount
humans = 4
# Bots ammount
bots = 0
#-------------------------------------------------

# Decks Generator, return as array, totalplayers = number of players + number of bots
def createDeck(totalplayers):

    # Creates the array "deck"
    deck = []

    # Creates the dictionary "deckset"
    # Defines cards types and how many you have in one deck with the
    # dictionary "deckset".
    deckset = {"Weed1": 10,
               "Weed2": 10,
               "Weed3": 6,
               "Weed4": 3,
               "Steal": 5,
               "WeedKiller": 5,
               "Dandelion": 5,
               "Hippie": 3,
               "Busted": 2,
               "Potzilla": 1}

    # Generates 1 extra deck every 4 totalplayers.
    ndecks = math.ceil(totalplayers/4)

    # This loops the same ammount of times as the numbers of decks above (ndecks).
    for i in range(0,int(ndecks)):

        # Iterates each card type in deckset dictionary
        for cardname, amount in deckset.iteritems():
            # And add an amount of them to the deck array
            deck.extend(amount * [cardname])

    # Shuffles the deck array
    shuffle(deck)

    return deck

# Play order generator
def createPlayOrder(humans,bots):

    # Defines the array to return the play order
    playorder = []

    # Add Humans
    if humans:
        for k in range(0,humans):
            playorder.append( "Human " + str(k + 1) )

    # Add Bots
    if bots:
        for k in range(0,bots):
            playorder.append( "Bot " + str(k + 1) )

    # Shuffle the array
    shuffle(playorder)

    return playorder

# Displays a GUI returning an action
def chooseAction():

    # Initializes GUI screen title
    title = player + " turn"

    # Initializes GUI message
    msg = ''

    # Displays all gardens in GUI message
    for who in gardens.keys():
        garden = gardens[who]
        msg += who + " Garden: "
        msg += ' - '.join(garden)
        msg += "\n"

    # Display current player's hand
    msg += "\n" + player + " hand:      " + ' - '.join(hands[player]) + "\n"

    # Initializes GUI choices
    choices = hands[player] + [" - End Turn"]

    # Inintializes GUI
    action = None
    while action == None:
        action = choicebox(msg, title, choices)

    return action

# Displays a GUI returning a target. exclude_self defines if the choice list will include the player taking the turn
def getTarget(exclude_self):

    # Initializes GUI screen title
    title = "Target " + action

    # Initializes GUI message
    msg = ''

    # Displays all gardens in GUI message
    for who in gardens.keys():
        garden = gardens[who]
        msg += who + " Garden: "
        msg += ' - '.join(garden)
        msg += "\n"

    # Initializes GUI choices and checks if exclude_self is True or False
    msg  += "\nSelect a target to use " + action
    if exclude_self:
        choices = [i for i in playorder if i != player]
    else:
        choices = [i for i in playorder if i]

    # Initializes GUI
    target = None
    while target == None:
        target = choicebox(msg, title, choices)
    return target

winner = None

#Initializes points and playorder
points = {}
playorder = createPlayOrder(humans,bots)
for player in playorder:
    points[player] = 0

# Main Loop
while winner == None:

    #Initialize new game
    totalplayers = humans + bots
    deck = createDeck(totalplayers)
    win = False
    cardposition = 0
    hands = {}
    gardens = {}
    shuffle(playorder)

    #Initialize players hands and gardens
    for player in playorder:
        hands[player] = []
        gardens[player] = []


    #Gives 5 cards for each player
    for player in playorder:
        print player
        for i in range(0,5):
            hands[player].append(deck[cardposition])
            cardposition +=1

    #Main loop for a round
    while win is False:

        #Main loop for a turn
        for player in playorder:

            # Checks if player is Busted.
            if any("Busted" in s for s in gardens[player]):
                gardens[player].remove("Busted")
                continue

            # Checks if deck has cards
            if cardposition != 50:
                hands[player].append(deck[cardposition])
                cardposition +=1

            # Main loop for choosing action
            action = chooseAction()
            while action != " - End Turn":

                if action == "Weed1":
                    if not any("Dandelion" in s for s in gardens[player]):
                        if len([card for card in gardens[player] if "Weed" in card]) < 5:
                            if any("Weed1" in s for s in hands[player]):
                                hands[player].remove("Weed1")
                                gardens[player].append("Weed1")

                elif action == "Weed2":
                    if not any("Dandelion" in s for s in gardens[player]):
                        if len([card for card in gardens[player] if "Weed" in card]) < 5:
                            if any("Weed2" in s for s in hands[player]):
                                hands[player].remove("Weed2")
                                gardens[player].append("Weed2")

                elif action == "Weed3":
                    if not any("Dandelion" in s for s in gardens[player]):
                        if len([card for card in gardens[player] if "Weed" in card]) < 5:
                            if any("Weed3" in s for s in hands[player]):
                                hands[player].remove("Weed3")
                                gardens[player].append("Weed3")

                elif action == "Weed4":
                    if not any("Dandelion" in s for s in gardens[player]):
                        if len([card for card in gardens[player] if "Weed" in card]) < 5:
                            if any("Weed4" in s for s in hands[player]):
                                hands[player].remove("Weed4")
                                gardens[player].append("Weed4")

                elif action == "Weed6":
                    if not any("Dandelion" in s for s in gardens[player]):
                        if len([card for card in gardens[player] if "Weed" in card]) < 5:
                            if any("Weed6" in s for s in hands[player]):
                                hands[player].remove("Weed6")
                                gardens[player].append("Weed6")

                elif action == "Dandelion":
                    if any("Dandelion" in s for s in hands[player]):

                        target = getTarget(True)
                        if not any("Dandelion" in s for s in gardens[target]):
                            hands[player].remove("Dandelion")
                            gardens[target].append("Dandelion")

                elif action == "WeedKiller":
                    if any("WeedKiller" in s for s in hands[player]):
                        target = getTarget(False)
                        if any("Dandelion" in s for s in gardens[target]):
                            gardens[target].remove("Dandelion")
                            hands[player].remove("WeedKiller")

                elif action == "Hippie":
                    if any("Hippie" in s for s in hands[player]):
                        target = getTarget(True)

                        if any("Weed1" in s for s in gardens[target]):
                            gardens[target].remove("Weed1")
                            hands[player].remove("Hippie")

                        elif any("Weed2" in s for s in gardens[target]):
                            gardens[target].remove("Weed2")
                            hands[player].remove("Hippie")

                        elif any("Weed3" in s for s in gardens[target]):
                            gardens[target].remove("Weed3")
                            hands[player].remove("Hippie")

                        elif any("Weed4" in s for s in gardens[target]):
                            gardens[target].remove("Weed4")
                            hands[player].remove("Hippie")

                        elif any("Weed6" in s for s in gardens[target]):
                            gardens[target].remove("Weed6")
                            hands[player].remove("Hippie")

                elif action == "Steal":
                    if any("Steal" in s for s in hands[player]):
                        target = getTarget(True)

                        if any("Weed6" in s for s in gardens[target]):
                            gardens[target].remove("Weed6")
                            gardens[player].append("Weed6")
                            hands[player].remove("Steal")

                        elif any("Weed4" in s for s in gardens[target]):
                            gardens[target].remove("Weed4")
                            gardens[player].append("Weed4")
                            hands[player].remove("Steal")

                        elif any("Weed3" in s for s in gardens[target]):
                            gardens[target].remove("Weed3")
                            gardens[player].append("Weed3")
                            hands[player].remove("Steal")

                        elif any("Weed2" in s for s in gardens[target]):
                            gardens[target].remove("Weed2")
                            gardens[player].append("Weed2")
                            hands[player].remove("Steal")

                        elif any("Weed1" in s for s in gardens[target]):
                            gardens[target].remove("Weed1")
                            gardens[player].append("Weed1")
                            hands[player].remove("Steal")

                elif action == "Busted":
                    if any("Busted" in s for s in hands[player]):
                        target = getTarget(True)

                        if not any("Busted" in s for s in gardens[target]):
                            hands[player].remove("Busted")
                            gardens[target].append("Busted")

                            if any("Weed6" in s for s in gardens[target]):
                                gardens[target].remove("Weed6")

                            elif any("Weed4" in s for s in gardens[target]):
                                gardens[target].remove("Weed4")

                            elif any("Weed3" in s for s in gardens[target]):
                                gardens[target].remove("Weed3")

                            elif any("Weed2" in s for s in gardens[target]):
                                gardens[target].remove("Weed2")

                            elif any("Weed1" in s for s in gardens[target]):
                                gardens[target].remove("Weed1")

                elif action == "Potzilla":
                    if any("Potzilla" in s for s in hands[player]):
                        target = getTarget(True)
                        hands[player].remove("Potzilla")

                        while any("Weed1" in s for s in gardens[target]):
                            gardens[target].remove("Weed1")

                        while any("Weed2" in s for s in gardens[target]):
                            gardens[target].remove("Weed2")

                        while any("Weed3" in s for s in gardens[target]):
                            gardens[target].remove("Weed3")

                        while any("Weed4" in s for s in gardens[target]):
                            gardens[target].remove("Weed4")

                        while any("Weed6" in s for s in gardens[target]):
                            gardens[target].remove("Weed6")

                        while any("Dandelion" in s for s in gardens[target]):
                            gardens[target].remove("Dandelion")

                        while any("Busted" in s for s in gardens[target]):
                            gardens[target].remove("Busted")

                action = chooseAction()

            # Checks if player won after ending his turn
            if len([card for card in gardens[player] if "Weed" in card]) >= 5:
                    win = True
                    break

    #Adds points
    for player in gardens.keys():

        while any("Weed1" in s for s in gardens[player]):
            gardens[player].remove("Weed1")
            actual = int(points[player])
            points[player] = actual + 1

        while any("Weed2" in s for s in gardens[player]):
            gardens[player].remove("Weed2")
            actual = int(points[player])
            points[player] = actual + 2

        while any("Weed3" in s for s in gardens[player]):
            gardens[player].remove("Weed3")
            actual = int(points[player])
            points[player] = actual + 3

        while any("Weed4" in s for s in gardens[player]):
            gardens[player].remove("Weed4")
            actual = int(points[player])
            points[player] = actual + 4

        while any("Weed6" in s for s in gardens[player]):
            gardens[player].remove("Weed6")
            actual = int(points[player])
            points[player] = actual + 6

    #Print points
    msg = ''
    for player in points:
        msg += player + " - "
        msg += str(points[player]) + " points"
        msg += "\n"
    msgbox(msg)

    #Checks for winner
    for player in points.keys():
        if points[player] >= 50:
            winner = player
            break

#Displays the Winner
msgbox ("Winner: " + player)
