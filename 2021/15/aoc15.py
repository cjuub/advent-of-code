from pathlib import Path
from networkx import DiGraph, dijkstra_path_length


def print_grid(g):
    for y in range(len(g)):
        for x in range(len(g[0])):
            print(g[y][x], end='')
        print()
    print()


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


lines = [x.strip() for x in Path('input.txt').open().readlines()]
w = len(lines[0])
h = len(lines)
grid = [[(int(lines[y][x])) for x in range(w)] for y in range(h)]

g = DiGraph()
for y in range(h):
    for x in range(w):
        g.add_node((x, y))
        for ay, ax in adjs_coord(grid, x, y):
            g.add_edge((x, y), (ax, ay), weight=grid[ay][ax])

l = dijkstra_path_length(g, (0, 0), (w-1, h-1))
print(f"Part 1: {l}")


grid = [[0 for x in range(w*5)] for y in range(h*5)]
for y in range(h * 5):
    y_risk = int(y/h)
    for x in range(w * 5):
        x_risk = int(x/w)
        if x_risk == 0 and y_risk == 0:
            grid[y][x] = int(lines[y][x])
        else:
            grid[y][x] = grid[y % h][x % w] + 1 * x_risk + 1 * y_risk
            grid[y][x] %= 9
        if grid[y][x] == 0:
            grid[y][x] = 9

g = DiGraph()
for y in range(h*5):
    for x in range(w*5):
        g.add_node((x, y))
        for ay, ax in adjs_coord(grid, x, y):
            g.add_edge((x, y), (ax, ay), weight=grid[ay][ax])
l = dijkstra_path_length(g, (0, 0), (w*5-1, h*5-1))
print(f"Part 2: {l}")
