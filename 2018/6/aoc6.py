#!/usr/bin/env python3

coordlist = []
with open('input.txt') as fp:
    for line in fp:
        inp = line.split(',')

        coordlist.append((int(inp[0]), int(inp[1])))

size = 500
grid = [[9999999 for i in range(size)] for j in range(size)]


def distance(x1, y1, x2, y2):
    dist = 0
    dist += abs(x1 - x2)
    dist += abs(y1 - y2)
    return dist


distmap = {}
old_dist = {}
for c in coordlist:
    for x in range(0, size):
        for y in range(0, size):
            dist = distance(x, y, c[0], c[1])

            if dist < grid[x][y]:
                grid[x][y] = dist
                distmap[str(x) + ',' + str(y)] = str(c[0]) + ',' + str(c[1])
            elif dist == grid[x][y]:
                old_dist[str(x) + ',' + str(y)] = grid[x][y]
                grid[x][y] = -1
                distmap[str(x) + ',' + str(y)] = ''
            elif grid[x][y] == -1:
                if dist < old_dist[str(x) + ',' + str(y)]:
                    grid[x][y] = dist
                    distmap[str(x) + ',' + str(y)] = str(c[0]) + ',' + str(c[1])

infs = []
for x in range(0, size):
    for y in [0, size-1]:
        if not str(x) + ',' + str(y) in infs:
            infs.append(distmap[str(x) + ',' + str(y)])

for y in range(0, size):
    for x in [0, size-1]:
        if not str(x) + ',' + str(y) in infs:
            infs.append(distmap[str(x) + ',' + str(y)])

cntmap = {}
for c in distmap.values():
    if c in infs:
        continue
    cntmap.setdefault(c, 0)
    cntmap[c] += 1

max_val = -1
for key, val in cntmap.items():
    if val > max_val:
        max_val = val
print(max_val)


reg_size = 0
for x in range(0, size):
    for y in range(0,size):
        dist = 0
        for c in coordlist:
            dist += distance(c[0], c[1], x, y)
            
        if dist < 10000:
            reg_size += 1

print(reg_size)
