from copy import deepcopy
from pathlib import Path

lines = [x.strip() for x in Path("input.txt").open("r").readlines()]

algo = lines[0]
lines = lines[2:]

w = len(lines[0])
h = len(lines)


def image_pixel(x, y):
    return [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x, y), (x + 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]


def calc_pixel(g, x, y):
    pix = image_pixel(x, y)
    binary = ""
    for pix_x, pix_y in pix:
        try:
            binary += "0" if g[pix_y][pix_x] == "." else "1"
        except IndexError:
            if algo[0] == ".":
                binary += "0"
            else:
                binary += "1"

    index = int(binary, 2)
    return algo[index]


def expand_grid(g):
    inf = 500
    half_inf = int(inf / 2)
    new_h = len(g) + inf
    new_w = len(g[0]) + inf
    new_g = [["." for x in range(new_w)] for y in range(new_h)]
    for y in range(half_inf, half_inf + len(g)):
        for x in range(half_inf, half_inf + len(g[0])):
            new_g[y][x] = g[y - half_inf - len(g)][x - half_inf - len(g[0])]

    return new_g, new_w, new_h


def shrink_grid(g):
    s = 4
    half_s = int(s / 2)
    new_h = len(g) - s
    new_w = len(g[0]) - s
    new_g = [["." for x in range(new_w)] for y in range(new_h)]
    for y in range(half_s, len(g) - half_s):
        for x in range(half_s, len(g[0]) - half_s):
            new_g[y - half_s][x - half_s] = g[y][x]

    return new_g, new_w, new_h


def run(grid, times):
    grid, w, h = expand_grid(grid)
    for i in range(times):
        grid_orig = deepcopy(grid)
        for y in range(h):
            for x in range(w):
                grid[y][x] = calc_pixel(grid_orig, x, y)

        grid, w, h = shrink_grid(grid)

    cnt = 0
    for y in range(h):
        for x in range(w):
            if grid[y][x] == "#":
                cnt += 1
    return cnt


grid = [[lines[y][x] for x in range(w)] for y in range(h)]
print(f"Part 1: {run(grid, 2)}")

grid = [[lines[y][x] for x in range(w)] for y in range(h)]
print(f"Part 2: {run(grid, 50)}")
