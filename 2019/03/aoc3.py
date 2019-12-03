#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

wires = []
for line in lines:
    wires.append(line.split(','))

def distance(x1, y1, x2, y2):
    dist = 0
    dist += abs(x1 - x2)
    dist += abs(y1 - y2)
    return dist

grid = [['.' for y in range(10000)] for x in range(10000)]

cx = 5000
cy = 5000

w1 = '-'
w2 = '='

cols = []
for wn in range(len(wires)):
    wire = wires[wn]

    x = cx
    y = cy
    for l in wire:
        if l[0] == 'R':
            for i in range(1, int(l[1:]) + 1):
                x += 1
                if grid[x][y] == '.':
                    grid[x][y] = wn
                elif grid[x][y] != 'X' and grid[x][y] != wn:
                    cols.append((x, y))
                    grid[x][y] = 'X'
        if l[0] == 'L':
            for i in range(1, int(l[1:]) + 1):
                x -= 1
                if grid[x][y] == '.':
                    grid[x][y] = wn
                elif grid[x][y] != 'X' and grid[x][y] != wn:
                    cols.append((x, y))
                    grid[x][y] = 'X'
        if l[0] == 'U':
            for i in range(1, int(l[1:]) + 1):
                y -= 1
                if grid[x][y] == '.':
                    grid[x][y] = wn
                elif grid[x][y] != 'X' and grid[x][y] != wn:
                    cols.append((x, y))
                    grid[x][y] = 'X'
        if l[0] == 'D':
            for i in range(1, int(l[1:]) + 1):
                y += 1
                if grid[x][y] == '.':
                    grid[x][y] = wn
                elif grid[x][y] != 'X' and grid[x][y] != wn:
                    cols.append((x, y))
                    grid[x][y] = 'X'

minv = 9999999999999
for col in cols:
    dist = distance(col[0], col[1], cx, cy)
    minv = min(dist, minv)

print('SOLUTION PART 1: ' + str(minv))

col_steps = []
for col in cols:
    for wn in range(len(wires)):
        wire = wires[wn]

        col_steps.append([])
        steps = 0

        x = cx
        y = cy
        for l in wire:
            if l[0] == 'R':
                for i in range(1, int(l[1:]) + 1):
                    x += 1
                    steps += 1
                    if x == col[0] and y == col[1]:
                        col_steps[wn].append(steps)
            if l[0] == 'L':
                for i in range(1, int(l[1:]) + 1):
                    x -= 1
                    steps += 1
                    if x == col[0] and y == col[1]:
                        col_steps[wn].append(steps)
            if l[0] == 'U':
                for i in range(1, int(l[1:]) + 1):
                    y -= 1
                    steps += 1
                    if x == col[0] and y == col[1]:
                        col_steps[wn].append(steps)
            if l[0] == 'D':
                for i in range(1, int(l[1:]) + 1):
                    y += 1
                    steps += 1
                    if x == col[0] and y == col[1]:
                        col_steps[wn].append(steps)

wn1 = col_steps[0]
wn2 = col_steps[1]
minv = 9999999999999
for i in range(len(wn1)):
    val = wn1[i] + wn2[i]
    minv = min(val, minv)

print('SOLUTION PART 2: ' + str(minv))
