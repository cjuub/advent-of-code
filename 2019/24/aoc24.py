#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

h = len(lines)
w = len(lines[0]) - 1
grid = [[' ' for y in range(w)] for x in range(h)]

for y2 in range(h):
    for x2 in range(w):
        grid[y2][x2] = lines[y2][x2]
        # print(grid[y2][x2], end='')
    # print()


def adjacents_to(x, y):
    return [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]


seen = set()
done = False
seen.add(str(grid))
while not done:

    grid2 = [[' ' for y in range(w)] for x in range(h)]
    for y2 in range(h):
        for x2 in range(w):
            grid2[y2][x2] = grid[y2][x2]

    for y2 in range(h):
        for x2 in range(w):
            adjs = adjacents_to(x2, y2)
            bugs = 0
            for adj in adjs:
                if adj[1] < 0 or adj[0] < 0:
                    continue
                try:
                    if grid2[adj[1]][adj[0]] == '#':
                        bugs += 1
                except:
                    pass

            if grid2[y2][x2] == '.' and (bugs == 1 or bugs == 2):
                grid[y2][x2] = '#'
                continue

            if grid2[y2][x2] == '#' and bugs != 1:
                grid[y2][x2] = '.'
                continue

    if not str(grid) in seen:
        seen.add(str(grid))
    else:
        done = True
        break


rating = 0
curr_pow = 1
for y2 in range(h):
    for x2 in range(w):
        if grid[y2][x2] == '#':
            rating += curr_pow
        curr_pow *= 2
print('Part 1: ' + str(rating))


size = 1000
levels = []
for i in range(size):
    empty_grid = [[' ' for y in range(w)] for x in range(h)]
    for y2 in range(h):
        for x2 in range(w):
            empty_grid[y2][x2] = '.'
    empty_grid[2][2] = '?'
    levels.append(empty_grid)


for y2 in range(h):
    for x2 in range(w):
        grid[y2][x2] = lines[y2][x2]
grid[2][2] = '?'

base_level_i = int(size / 2)
levels[base_level_i] = grid


def copy_grid(g):
    g2 = [[' ' for y in range(w)] for x in range(h)]
    for y2 in range(h):
        for x2 in range(w):
            g2[y2][x2] = g[y2][x2]

    return g2


def adjacents_to_part2(x, y):
    adjs = set()
    if 0 < x < w - 1 and 0 < y < h - 1:
        if (x, y - 1) != (2, 2):
            adjs.add((x, y - 1, 0))  # above
        else:
            for x2 in range(w):
                adjs.add((x2, h - 1, -1))
        if (x - 1, y) != (2, 2):
            adjs.add((x - 1, y, 0))  # left
        else:
            for y2 in range(h):
                adjs.add((w - 1, y2, -1))
        if (x + 1, y) != (2, 2):
            adjs.add((x + 1, y, 0))  # right
        else:
            for y2 in range(h):
                adjs.add((0, y2, -1))
        if (x, y + 1) != (2, 2):
            adjs.add((x, y + 1, 0))  # below
        else:
            for x2 in range(w):
                adjs.add((x2, 0, -1))
    if y == 0:
        adjs.add((2, 1, 1))
        if 0 < x < w - 1:
            adjs.add((x, y + 1, 0))  # below
            adjs.add((x - 1, y, 0))  # left
            adjs.add((x + 1, y, 0))  # right
        elif x == 0:
            adjs.add((1, 2, 1))
            adjs.add((x, y + 1, 0))  # below
            adjs.add((x + 1, y, 0))  # right
        elif x == w - 1:
            adjs.add((3, 2, 1))
            adjs.add((x, y + 1, 0))  # below
            adjs.add((x - 1, y, 0))  # left
        else:
            assert False
    elif y == h - 1:
        adjs.add((2, 3, 1))
        if 0 < x < w - 1:
            adjs.add((x, y - 1, 0))  # above
            adjs.add((x - 1, y, 0))  # left
            adjs.add((x + 1, y, 0))  # right
        elif x == 0:
            adjs.add((1, 2, 1))
            adjs.add((x, y - 1, 0))  # above
            adjs.add((x + 1, y, 0))  # right
        elif x == w - 1:
            adjs.add((3, 2, 1))
            adjs.add((x, y - 1, 0))  # above
            adjs.add((x - 1, y, 0))  # left
        else:
            assert False
    if x == 0:
        adjs.add((1, 2, 1))
        if 0 < y < h - 1:
            adjs.add((x, y - 1, 0))  # above
            adjs.add((x + 1, y, 0))  # right
            adjs.add((x, y + 1, 0))  # below
    elif x == w - 1:
        adjs.add((3, 2, 1))
        if 0 < y < h - 1:
            adjs.add((x, y - 1, 0))  # above
            adjs.add((x - 1, y, 0))  # left
            adjs.add((x, y + 1, 0))  # below

    return adjs


def bug_cnt(level, orig_levels):
    grid_new = copy_grid(orig_levels[level])

    for y2 in range(h):
        for x2 in range(w):
            adjs = adjacents_to_part2(x2, y2)
            bugs = 0

            for adj in adjs:
                g2 = orig_levels[level + adj[2]]
                if g2[adj[1]][adj[0]] == '#':
                    bugs += 1

            if levels[level][y2][x2] == '.' and (bugs == 1 or bugs == 2):
                grid_new[y2][x2] = '#'
                continue

            if levels[level][y2][x2] == '#' and bugs != 1:
                grid_new[y2][x2] = '.'
                continue

    return grid_new


for min in range(200):
    new_levels = []
    new_levels.append(levels[0])
    for level in range(1, size - 1):
        new_levels.append(bug_cnt(level, levels))
    new_levels.append(levels[size - 1])

    assert '#' not in str(levels[0])
    assert '#' not in str(levels[size - 1])

    levels = new_levels

# for level in [502, 501, 500, 499, 498]:
#     g = levels[level]
#     for y2 in range(h):
#         for x2 in range(w):
#             print(g[y2][x2], end='')
#         print()
#     print()

cnt = 0
for level in range(size):
    g = levels[level]
    for y2 in range(h):
        for x2 in range(w):
            if g[y2][x2] == '#':
                cnt += 1

print('Part 2: ' + str(cnt))
