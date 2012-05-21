#!/usr/bin/env python

import random

class MontyHall:
    "Simulate a game in the Monty Hall problem."

    def __init__(self):
        self.rng = random.Random()
        self.setupDoorPermutations()

    def setupDoorPermutations(self):
        "Permutations of goat1, goat2, and car used in the game."
        self.doorPermutations = (
            ('goat1', 'goat2', 'car'),
            ('goat1', 'car',   'goat2'),
            ('goat2', 'goat1', 'car'),
            ('goat2', 'car',   'goat1'),
            ('car',   'goat1', 'goat2'),
            ('car',   'goat2', 'goat1')
        )

    def setupDoors(self):
        "Setup the doors containing the goats and car." 
        # use random number generator to pick one of the door permutations
        rand_door_permutation = self.rng.randint(0,5)
        self.doors = self.doorPermutations[rand_door_permutation]

    def door(self, ind):
        "Return a door number given an index."
        return ind+1

    def ind(self, door):
        "Return an index given a door number."
        return door-1

    def isWinner(self, door):
        "Return true when the player has won the game."
        return self.doors[self.ind(door)] == 'car'

    def winningDoor(self):
        "Return the door number containing the car."
        return self.door( self.doors.index('car') )

    def switchDoor(self, door):
        "Switch the door selected by the player."
        if self.isWinner(door):
            # since the user is switching away from the winning door,
            # randomly choose between one of the two available goats
            choices = [ (2,3), (1,3), (1,2) ]
            choose = choices[self.ind(door)]
            # use random number generator to pick one of the door choices
            rand_choice = self.rng.randint(0,1)
            door = choose[rand_choice]
        else:
            # the host will never show the door containing the car,
            # so the user will always select the door containing the car
            door = self.winningDoor()
        return door

    def game(self, door, switch_door):
        "Play a single game and return the outcome."
        self.setupDoors()
        if switch_door:
            door = self.switchDoor(door)
        return self.isWinner(door)

    def randDoor(self):
        "Help the user by picking a random door to start."
        return self.rng.randint(1,3)

def pcnt(num, denom, scale=100.0):
    "Return number as percent from [0.0, scale]"
    return num*scale/denom

def main():
    switch_door = True
    games = 10000
    monty_hall = MontyHall()
    outcomes = [None] * games   # history of game outcomes
    picked = [None] * games     # history of doors picked by user
    winning = [None] * games    # history of winning door
    verbose = True

    for g in range(games):
        # use random number generator to pick a door (not strictly necessary)
        door = monty_hall.randDoor()
        outcomes[g] = monty_hall.game(door, switch_door)
        if verbose:
            picked[g] = door
            winning[g] = monty_hall.winningDoor()

    won = sum(outcomes)
    lost = games - won
    print('games\n count=%-5d\n won=%-5d(%3.1f)\n lost=%-5d(%3.1f)' % 
        (games, won, pcnt(won,games), lost, pcnt(lost,games)))

    if verbose:
        reports = [ ('picked', picked), ('winning', winning) ]
        for name,raw in reports:
            counts = [raw.count(door) for door in range(1,4)]
            pcnts  = [pcnt(count, games) for count in counts]
            print('%s\n door1=%-5d(%3.1f)\n door2=%-5d(%3.1f)\n door3=%-5d(%3.1f)' %
                (name, counts[0], pcnts[0], counts[1], pcnts[1], counts[2], pcnts[2]))

if __name__ == '__main__':
    main()

