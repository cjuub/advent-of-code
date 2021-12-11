from pathlib import Path

def print_grid(g):
    for y in range(len(g)):
        for x in range(len(g[0])):
            print(g[y][x], end='')
        print()
    print()


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

    if y < len(g) - 1 and x < len(g[0]) - 1:
        res.append((y + 1, x + 1))
    if y > 0 and x < len(g[0]) - 1:
        res.append((y - 1, x + 1))
    if y < len(g) - 1 and x > 0:
        res.append((y + 1, x - 1))
    if y > 0 and x > 0:
        res.append((y - 1, x - 1))

    return res


lines = [x.strip() for x in Path("input.txt").open().readlines()]
w = len(lines[0])
h = len(lines)
grid = [[int(lines[y][x]) for x in range(w)] for y in range(h)]


def has_charged(g):
    for y in range(h):
        for x in range(w):
            if g[y][x] > 9:
                return True
    return False


flashes = 0
for t in range(100):
    grid = [[grid[y][x] + 1 for x in range(w)] for y in range(h)]
    while has_charged(grid):
        for y in range(h):
            for x in range(w):
                if grid[y][x] > 9:
                    grid[y][x] = 0
                    flashes += 1
                    for ay, ax in adjs_coord(grid, x, y):
                        if grid[ay][ax] != 0:
                            grid[ay][ax] += 1

print(f"Part 1: {flashes}")


grid = [[int(lines[y][x]) for x in range(w)] for y in range(h)]
for t in range(1000):
    is_all_zero = True
    for y in range(h):
        for x in range(w):
            if not grid[y][x] == 0:
                is_all_zero = False
                break
        if not is_all_zero:
            break

    if is_all_zero:
        print(f"Part 2: {t}")
        break

    grid = [[grid[y][x] + 1 for x in range(w)] for y in range(h)]
    while has_charged(grid):
        for y in range(h):
            for x in range(w):
                if grid[y][x] > 9:
                    grid[y][x] = 0
                    flashes += 1
                    for ay, ax in adjs_coord(grid, x, y):
                        if grid[ay][ax] != 0:
                            grid[ay][ax] += 1

