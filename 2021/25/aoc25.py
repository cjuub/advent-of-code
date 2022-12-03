from copy import deepcopy
from pathlib import Path

lines = [x.strip() for x in Path("input.txt").open("r").readlines()]
w = len(lines[0])
h = len(lines)


def print_grid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] != 0:
                print(grid[y][x], end='')
            else:
                print('.', end='')
        print()
    print()


g = [["." for x in range(w)] for y in range(h)]
for y in range(h):
    for x in range(w):
        g[y][x] = lines[y][x]


def can_move_east(grid, pos):
    if pos[0] + 1 == w:
        return grid[y][0] == ".", (0, y)
    return grid[y][x+1] == ".", (x+1, y)


def can_move_south(grid, pos):
    if pos[1] + 1 == h:
        return grid[0][x] == ".", (x, 0)
    return grid[y+1][x] == ".", (x, y+1)


i = 0
while True:
    new_g = deepcopy(g)
    move_cnt = 0
    for y in range(h):
        for x in range(w):
            res = False
            next_x, next_y = (0, 0)
            if g[y][x] == ">":
                res, (next_x, next_y) = can_move_east(g, (x, y))
            else:
                continue

            if res:
                new_g[next_y][next_x] = g[y][x]
                new_g[y][x] = "."
                move_cnt += 1

    g = deepcopy(new_g)

    for y in range(h):
        for x in range(w):
            res = False
            next_x, next_y = (0, 0)
            if g[y][x] == "v":
                res, (next_x, next_y) = can_move_south(g, (x, y))
            else:
                continue

            if res:
                new_g[next_y][next_x] = g[y][x]
                new_g[y][x] = "."
                move_cnt += 1

    i += 1
    if move_cnt == 0:
        break
    g = deepcopy(new_g)

print(f"Part 1: {i}")
