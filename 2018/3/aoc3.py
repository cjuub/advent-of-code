#!/usr/bin/env python3

grid = [[0 for _ in range(1000)] for _ in range(1000)]

cnt = 0
with open('input.txt') as fp:
    for line in fp:
        entry = line.split(' ')
        claim_id = entry[0]
        x0, y0 = tuple([int(x) for x in entry[2][:-1].split(',')])
        width, height = tuple([int(y) for y in entry[3].split('x')])

        for x in range(x0, x0 + width):
            for y in range(y0, y0 + height):
                if grid[x][y] == 1:
                    cnt += 1

                grid[x][y] += 1

with open('input.txt') as fp:
    for line in fp:
        entry = line.split(' ')
        claim_id = entry[0]
        x0, y0 = tuple([int(x) for x in entry[2][:-1].split(',')])
        width, height = tuple([int(y) for y in entry[3].split('x')])

        overlaps = False
        for x in range(x0, x0 + width):
            for y in range(y0, y0 + height):
                if grid[x][y] > 1:
                    overlaps = True

        if not overlaps:
            print('Claim not overlapping: ' + claim_id)

print(cnt)

