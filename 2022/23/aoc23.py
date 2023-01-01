from collections import deque
from pathlib import Path


def print_grid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            print(grid[y][x], end='')
        print()
    print()


def adjacents(x, y):
    return [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]


def north_adjacents(x, y):
    return [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]


def south_adjacents(x, y):
    return [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]


def west_adjacents(x, y):
    return [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1)]


def east_adjacents(x, y):
    return [(x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]


lines = [x.strip() for x in Path("input.txt").open("r").readlines()]

side = 200
side_half = int(side / 2)
init_len = len(lines)
init_len_half = int(init_len / 2)

g = [["." for x in range(side)] for y in range(side)]
for y in range(side_half - init_len_half - 1, side_half + init_len_half - 1):
    for x in range(side_half - init_len_half - 1, side_half + init_len_half - 1):
        g[y][x] = lines[y - side_half + init_len_half + 1][x - side_half + init_len_half + 1]


proposed_directions = deque([north_adjacents, south_adjacents, west_adjacents, east_adjacents])
direction_targets = deque([lambda x, y: (x, y - 1), lambda x, y: (x, y + 1), lambda x, y: (x - 1, y), lambda x, y: (x + 1, y)])

for i in range(10):
    proposed = []
    for y in range(side):
        for x in range(side):
            if g[y][x] == "#":
                any_adjacent_elf = False
                for ax, ay in adjacents(x, y):
                    if g[ay][ax] == "#":
                        any_adjacent_elf = True
                        break
                if not any_adjacent_elf:
                    continue

                if "#" not in [g[ay][ax] for (ax, ay) in proposed_directions[0](x, y)]:
                    proposed.append(((x, y), direction_targets[0](x, y)))
                elif "#" not in [g[ay][ax] for (ax, ay) in proposed_directions[1](x, y)]:
                    proposed.append(((x, y), direction_targets[1](x, y)))
                elif "#" not in [g[ay][ax] for (ax, ay) in proposed_directions[2](x, y)]:
                    proposed.append(((x, y), direction_targets[2](x, y)))
                elif "#" not in [g[ay][ax] for (ax, ay) in proposed_directions[3](x, y)]:
                    proposed.append(((x, y), direction_targets[3](x, y)))

    for (x1, y1), (px1, py1) in proposed:
        unique_proposal = True
        for (x2, y2), (px2, py2) in proposed:
            if (x1, y1) == (x2, y2):
                continue
            if (px1, py1) == (px2, py2):
                unique_proposal = False
                break
        if unique_proposal:
            g[y1][x1] = "."
            g[py1][px1] = "#"

    proposed_directions.rotate(-1)
    direction_targets.rotate(-1)


x_min = 999999999
x_max = 0
y_min = 999999999
y_max = 0
for y in range(side):
    for x in range(side):
        if g[y][x] == "#":
            x_min = min(x, x_min)
            x_max = max(x + 1, x_max)
            y_min = min(y, y_min)
            y_max = max(y + 1, y_max)

cnt = 0
for y in range(y_min, y_max):
    for x in range(x_min, x_max):
        if g[y][x] == ".":
            cnt += 1

print(f"Part 1: {cnt}")

g = [["." for x in range(side)] for y in range(side)]
for y in range(side_half - init_len_half - 1, side_half + init_len_half - 1):
    for x in range(side_half - init_len_half - 1, side_half + init_len_half - 1):
        g[y][x] = lines[y - side_half + init_len_half + 1][x - side_half + init_len_half + 1]


proposed_directions = deque([north_adjacents, south_adjacents, west_adjacents, east_adjacents])
direction_targets = deque([lambda x, y: (x, y - 1), lambda x, y: (x, y + 1), lambda x, y: (x - 1, y), lambda x, y: (x + 1, y)])

i = 0
while True:
    proposed = []
    for y in range(side):
        for x in range(side):
            if g[y][x] == "#":
                any_adjacent_elf = False
                for ax, ay in adjacents(x, y):
                    if g[ay][ax] == "#":
                        any_adjacent_elf = True
                        break
                if not any_adjacent_elf:
                    continue

                if "#" not in [g[ay][ax] for (ax, ay) in proposed_directions[0](x, y)]:
                    proposed.append(((x, y), direction_targets[0](x, y)))
                elif "#" not in [g[ay][ax] for (ax, ay) in proposed_directions[1](x, y)]:
                    proposed.append(((x, y), direction_targets[1](x, y)))
                elif "#" not in [g[ay][ax] for (ax, ay) in proposed_directions[2](x, y)]:
                    proposed.append(((x, y), direction_targets[2](x, y)))
                elif "#" not in [g[ay][ax] for (ax, ay) in proposed_directions[3](x, y)]:
                    proposed.append(((x, y), direction_targets[3](x, y)))

    move_cnt = 0
    for (x1, y1), (px1, py1) in proposed:
        unique_proposal = True
        for (x2, y2), (px2, py2) in proposed:
            if (x1, y1) == (x2, y2):
                continue
            if (px1, py1) == (px2, py2):
                unique_proposal = False
                break
        if unique_proposal:
            move_cnt += 1
            g[y1][x1] = "."
            g[py1][px1] = "#"

    if move_cnt == 0:
        break

    proposed_directions.rotate(-1)
    direction_targets.rotate(-1)
    i += 1

print_grid(g)
print(f"Part 2: {i + 1}")
