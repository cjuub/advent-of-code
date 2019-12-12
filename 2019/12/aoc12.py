#!/usr/bin/env python3
import math


# stack overflow for getting smallest multiple of all cycles
# https://stackoverflow.com/questions/51716916/built-in-module-to-calculate-least-common-multiple
def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


with open('input.txt') as fp:
    lines = fp.readlines()

moonpos = []
for line in lines:
    split = line.split(' ')
    moonpos.append([int(split[0].strip()[3:-1]),
                    int(split[1].strip()[2:-1]),
                    int(split[2].strip()[2:-1])])

totals = []
moonvel = [[0, 0, 0],
           [0, 0, 0],
           [0, 0, 0],
           [0, 0, 0]]
for i in range(1000):
    for j, moon in enumerate(moonpos):
        for k, moon2 in enumerate(moonpos):
            if j == k:
                continue

            for coord in range(3):
                if moon[coord] < moon2[coord]:
                    moonvel[j][coord] += 1
                elif moon[coord] > moon2[coord]:
                    moonvel[j][coord] -= 1

    for j, moon in enumerate(moonpos):
        for coord in range(3):
            moon[coord] += moonvel[j][coord]

    totals = []
    for j, moon in enumerate(moonpos):
        pot = abs(moon[0]) + abs(moon[1]) + abs(moon[2])
        kin = abs(moonvel[j][0]) + abs(moonvel[j][1]) + abs(moonvel[j][2])
        totals.append(pot * kin)

print('Part 1: ' + str(sum(totals)))

moonpos = []
origs = []
for line in lines:
    split = line.split(' ')
    moonpos.append([int(split[0].strip()[3:-1]),
                    int(split[1].strip()[2:-1]),
                    int(split[2].strip()[2:-1])])

moonvel = [[0, 0, 0],
           [0, 0, 0],
           [0, 0, 0],
           [0, 0, 0]]

seen = [set(), set(), set()]
cycles = [-1, -1, -1]
last_cycles = [-1, -1, -1]
for i in range(10000000):
    last_cycles = cycles[:]
    for j, moon in enumerate(moonpos):
        for k, moon2 in enumerate(moonpos):
            if j == k:
                continue

            for coord in [0, 1, 2]:
                if moon[coord] < moon2[coord]:
                    moonvel[j][coord] += 1
                elif moon[coord] > moon2[coord]:
                    moonvel[j][coord] -= 1

    for coord in range(3):
        for j, moon in enumerate(moonpos):
            moon[coord] += moonvel[j][coord]

        entry = ''
        for j, moon in enumerate(moonpos):
            entry += str(moon[coord]) + ' ' + str(moonvel[j][coord]) + ' '

        if entry not in seen[coord]:
            cycles[coord] = i + 1

        seen[coord].add(entry)

    if cycles == last_cycles:
        break

print('Part 2: ' + str(lcm(lcm(cycles[0], cycles[1]), cycles[2])))
