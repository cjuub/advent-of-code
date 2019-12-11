#!/usr/bin/env python3
import math

with open('input.txt') as fp:
    lines = fp.readlines()

grid = [['.' for y in range(len(lines[0]) - 1)] for x in range(len(lines))]

for y in range(len(grid[0])):
    for x in range(len(grid)):
        grid[y][x] = lines[y][x]
        print(lines[y][x], end='')
    print()

best_cnt = -1
best = (-1, -1)
checked_sets = {}
for y in range(len(grid)):
    for x in range(len(grid[0])):
        if grid[y][x] != '#':
            continue

        checked = set()
        for y2 in range(len(grid)):
            for x2 in range(len(grid[0])):
                if grid[y2][x2] != '#':
                    continue

                if x == x2 and y == y2:
                    continue

                dx = x2 - x
                dy = y2 - y
                gcd = math.gcd(dx, dy)
                gcd = 1 if gcd < 1 else gcd
                checked.add((dx / gcd, dy / gcd))

        if len(checked) > best_cnt:
            best_cnt = len(checked)
            best = (x, y)

        checked_sets[(x, y)] = checked

print('Part 1: ' + str(len(checked_sets[best])))

angle_list = []
for dx, dy in checked_sets[best]:
    angle = math.atan2(dx, dy)
    entry = (angle, (dx, dy))
    angle_list.append(entry)

angle_list = sorted(angle_list)
ast_200 = angle_list[-200][1]
x = int(best[0] + ast_200[0])
y = int(best[1] + ast_200[1])

print('Part 2: ' + str(x * 100 + y))
