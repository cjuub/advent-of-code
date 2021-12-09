from pathlib import Path


def print_grid(g):
    for y in range(len(g)):
        for x in range(len(g[0])):
            print(g[y][x], end='')
        print()
    print()


lines = [x.strip() for x in Path("input.txt").open().readlines()]

w = len(lines[0])
h = len(lines)

grid = [[-1 for x in range(w)] for y in range(h)]

for y in range(h):
    for x in range(w):
        grid[y][x] = int(lines[y][x])


def adjs(g, x, y):
    res = []
    if x > 0:
        res.append(g[y][x-1])
    if x < len(g[0]) - 1:
        res.append(g[y][x+1])
    if y > 0:
        res.append(g[y-1][x])
    if y < len(g) - 1:
        res.append(g[y+1][x])

    return res


lows = []
for y in range(h):
    for x in range(w):
        is_low = True
        for adj in adjs(grid, x, y):
            if grid[y][x] >= adj:
                is_low = False

        if is_low:
            lows.append(grid[y][x])

sum = 0
for low in lows:
    sum += low + 1

print(f"Part 1: {sum}")


def adjs_coord(g, x, y):
    res = []
    if x > 0:
        res.append((y, x - 1))
    if x < len(g[0]) - 1:
        res.append((y, x + 1))
    if y > 0:
        res.append((y - 1, x))
    if y < len(g) - 1:
        res.append((y + 1, x))

    return res


def basin(g, x, y, b):
    if g[y][x] == 9:
        return []

    b.append(g[y][x])
    g[y][x] = 9
    for ay, ax in adjs_coord(g, x, y):
        basin(g, ax, ay, b)

    return b


basins = []
for y in range(h):
    for x in range(w):
        b = basin(grid, x, y, [])
        if b:
            basins.append(b)

basins = sorted(basins, key=lambda x: len(x), reverse=True)
print(f"Part 2: {len(basins[0]) * len(basins[1]) * len(basins[2])}")
