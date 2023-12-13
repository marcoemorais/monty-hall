#!/usr/bin/env python

from secrets import randbelow


class MontyHall:
    "Simulate a game in the Monty Hall problem."

    def __init__(self):
        self.door_permutations = (
            ('goat', 'goat', 'car'),
            ('goat', 'car',   'goat'),
            ('car',   'goat', 'goat')
        )
        self.doors = None
        self.winning_door = None

    def door(self, ind):
        "Return a door number given an index."
        return ind+1

    def ind(self, door):
        "Return an index given a door number."
        return door-1

    def is_winner(self, door):
        "Return true when the player has won the game."
        return self.doors[self.ind(door)] == 'car'

    def switch_door(self, door):
        "Switch the door selected by the player."
        if self.is_winner(door):
            # since the user is switching away from the winning door,
            # randomly choose between one of the two available goats
            choices = [(2, 3), (1, 3), (1, 2)]
            choose = choices[self.ind(door)]
            # use random number generator to pick one of the door choices
            return choose[randbelow(2)]
        return self.winning_door

    def game(self, door, switch_door):
        "Play a single game and return the outcome."
        self.doors = self.door_permutations[randbelow(3)]
        self.winning_door = self.door(self.doors.index('car'))
        if switch_door:
            door = self.switch_door(door)
        return self.is_winner(door)


def pcnt(num, denom, scale=100.0):
    "Return number as percent from [0.0, scale]"
    return num*scale/denom


def main():
    "Main function"
    switch_door = True
    games = 10000
    monty_hall = MontyHall()
    outcomes = [None] * games   # history of game outcomes
    picked = [None] * games     # history of doors picked by user
    winning = [None] * games    # history of winning door
    verbose = True

    for g in range(games):
        # use random number generator to pick a door (not strictly necessary)
        door = randbelow(3) + 1
        outcomes[g] = monty_hall.game(door, switch_door)
        if verbose:
            picked[g] = door
            winning[g] = monty_hall.winning_door

    won = sum(outcomes)
    lost = games - won
    print(f'Games:\n count = {games}\n won = {won} ({pcnt(won, games)}%)\n lost = {lost} ({pcnt(lost, games)}%)')

    if verbose:
        reports = [('\nPicked:', picked), ('\nWinning:', winning)]
        for name, raw in reports:
            counts = [raw.count(door) for door in range(1, 4)]
            pcnts = [pcnt(count, games) for count in counts]
            print(f'{name}\n door1 = {counts[0]} ({pcnts[0]}%)\n door2 = {counts[1]} ({pcnts[1]}%)\n door3 = {counts[2]} ({pcnts[2]}%)')


if __name__ == '__main__':
    main()