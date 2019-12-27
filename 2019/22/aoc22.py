#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

cards = []
for i in range(10007):
    cards.append(i)


def deal_into_new_stack(cards):
    cards_2 = []
    while True:
        try:
            cards_2.append(cards.pop())
        except:
            return cards_2


def cut(cards, n):
    first = cards[:n]
    rem = cards[n:]
    return rem + first


def deal_with_incr(cards, n):
    cards_2 = [-1] * len(cards)
    i = 0
    for card in cards:
        cards_2[i % len(cards)] = card
        i += n

    return cards_2


for line in lines:
    if line.startswith('cut'):
        cards = cut(cards, int(line.split(' ')[1]))
    elif line.startswith('deal with increment'):
        cards = deal_with_incr(cards, int(line.split(' ')[-1]))
    else:
        cards = deal_into_new_stack(cards)

print('Part 1: ' + str(cards.index(2019)))


# This class saw many implementations before working...
# Had to look up a lot of clues to get it working. Got as long as simulating the deck one iteration without
# simulating the deck though (without looking anything up)! TOO HARD FOR AOC!
class Shuffle:
    def __init__(self, size, index, operations):
        self.size = size
        self.index = index
        self.operations = operations
        self.res = self.index
        self.offset = 0
        self.increment = 1
        self.iterations = 1

    def shuffle(self):
        for operation, arg in operations:
            operation(self, arg)

        return 0, self.offset, self.increment

    def deal_into_new_stack(self, n):
        self.increment = (self.increment * -1) % self.size
        self.offset = (self.offset + self.increment) % self.size

    def cut(self, n):
        self.offset = (self.offset + n * self.increment) % self.size

    def deal_with_incr(self, n):
        self.increment = (self.increment * inv(n, self.size) % self.size)


# stackoverflow
def inv(x, m):
    return pow(x, m - 2, m)


operations = []
for i in range(1):
    for line in lines:
        if line.startswith('cut'):
            operations.append((Shuffle.cut, int(line.split(' ')[1])))
        elif line.startswith('deal with increment'):
            operations.append((Shuffle.deal_with_incr, int(line.split(' ')[-1])))
        else:
            operations.append((Shuffle.deal_into_new_stack, -1))


size = 119315717514047
shuffle = Shuffle(size, 2020, operations)
res, offset, increment = shuffle.shuffle()

incr = pow(increment, 101741582076661, size)
offs = offset * (1 - pow(increment, 101741582076661, size)) * inv(1 - increment, size)
print('Part 2: ' + str((2020 * incr + offs) % size))
