#!/usr/bin/env python3


class Marble:
    def __init__(self, nbr, prev, next):
        self.nbr = nbr
        self.prev = prev
        self.next = next

    def __repr__(self):
        return str(self.nbr)


def print_circle():
    first = circle
    next = circle.next
    print(first, end=' ')
    while first != next:
        print(next, end=' ')
        next = next.next
    print()


marbles = []
last_worth = 0
nbr_players = 0
with open('input.txt') as fp:
    for line in fp:
        nbr_players = int(line.split()[0])
        last_worth = int(line.split()[6])


for x in [1, 100]:
    circle = Marble(0, None, None)
    circle.prev = circle
    circle.next = circle

    curr_marble = circle
    player_scores = [0 for x in range(nbr_players)]
    i = 1
    while i != last_worth * x:
        next = curr_marble.next
        two_next = next.next

        new = Marble(i, next, two_next)

        if new.nbr % 23 == 0:
            player_scores[i % nbr_players] += new.nbr

            rem = curr_marble
            for j in range(7):
                rem = rem.prev

            player_scores[i % nbr_players] += rem.nbr
            rem.prev.next = rem.next
            rem.next.prev = rem.prev

            curr_marble = rem.next
        else:
            next.next = new
            two_next.prev = new
            curr_marble = new

        i += 1

    max_score = 0
    max_index = -1
    for score in range(len(player_scores)):
        if player_scores[score] > max_score:
            max_score = player_scores[score]
            max_index = score

    print(max_score)
