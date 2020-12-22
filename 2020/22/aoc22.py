#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

p1 = []
p2 = []
curr_p = p1
for line in lines:
    line = line.strip()

    if line.startswith('Player'):
        continue
    
    if line == '':
        curr_p = p2
        continue

    curr_p.append(int(line))

p1_orig = p1[:]
p2_orig = p2[:]

round = 0
while len(p1) != 0 and len(p2) != 0:
    p1_played = p1[0]
    p1 = p1[1:]
    p2_played = p2[0]
    p2 = p2[1:]

    if p1_played > p2_played:
        p1.append(p1_played)
        p1.append(p2_played)
    elif p2_played > p1_played:
        p2.append(p2_played)
        p2.append(p1_played)
    else:
        print('draw')
        break

    round += 1

winner = p1 if len(p2) == 0 else p2

score = 0
for i, card in enumerate(reversed(winner)):
    score += card * (i+1)

print(f'Part 1: {score}')


def play(p1, p2):
    round = 0
    prevs = set()
    while True:
        if (tuple(p1), tuple(p2)) in prevs:
            return 'p1', p1
        else:
            prevs.add((tuple(p1), tuple(p2)))

        p1_played = p1.pop(0)
        p2_played = p2.pop(0)

        if len(p1) >= p1_played and len(p2) >= p2_played:
            round_winner = play(p1[:p1_played], p2[:p2_played])
        else:
            round_winner = ('p1', p1) if p1_played > p2_played else ('p2', p2)

        if round_winner[0] == 'p1':
            p1.append(p1_played)
            p1.append(p2_played)
        else:
            p2.append(p2_played)
            p2.append(p1_played)

        if len(p1) == 0:
            return 'p2', p2

        if len(p2) == 0:
            return 'p1', p1

        round += 1

p1 = p1_orig
p2 = p2_orig

winner = play(p1, p2)

score = 0
for i, card in enumerate(reversed(winner[1])):
    score += card * (i+1)

print(f'Part 2: {score}')
