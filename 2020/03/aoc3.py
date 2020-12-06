#!/usr/bin/env python3

input = []
with open('input.txt') as fp:
    for line in fp:
        input.append(list(line.strip()))
        
grid = [['' for y in range(len(input))] for x in range(len(input[0]))]
for y in range(len(input)):
    for x in range(len(input[0])):
        grid[x][y] = input[y][x]

cnt = 0
next = (3, 1)
for y in range(len(grid[0])):
    for x in range(10000):
        if (x, y) == next:
            if grid[x % len(grid)][y] == '#':
                cnt += 1
            next = (x + 3, y + 1)

print('Part 1: {}'.format(cnt))

prod = 1
for change in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
    cnt = 0
    next = change
    for y in range(len(grid[0])):
        for x in range(10000):
            if (x, y) == next:
                if grid[x % len(grid)][y] == '#':
                    cnt += 1
                next = (x + change[0], y + change[1])
    prod = prod * cnt

print('Part 2: {}'.format(prod))
