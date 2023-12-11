from enum import Enum
from pathlib import Path
from networkx import Graph, all_pairs_shortest_path_length, all_pairs_dijkstra_path_length

lines = Path("input.txt").read_text().splitlines()

orig_w = len(lines[0])
orig_h = len(lines)
w = orig_w
h = orig_h

grid = [[lines[y][x] for x in range(w)] for y in range(h)]

def print_grid(grid, w, h):
    for y in range(h):
        for x in range(w):
            print(grid[y][x], end="")
        print()
    print()

def is_empty_row(grid, y, w):
    for x in range(w):
        if grid[y][x] not in [".", "R", "C", "X"]:
            return False
    return True

def is_empty_column(grid, x, h):
    for y in range(h):
        if grid[y][x] not in [".", "R", "C", "X"]:
            return False
    return True


def expand(grid, w, h):
    expanded_grid = []
    for y in range(h):
        expanded_grid.append(grid[y][:])
        if is_empty_row(grid, y, h):
            expanded_grid.append(grid[y][:])

    expanded_h = len(expanded_grid)

    x = 0
    while x < len(expanded_grid[0]):
        was_expanded = False
        if is_empty_column(expanded_grid, x, expanded_h):
            was_expanded = True
            for y in range(expanded_h):
                expanded_grid[y].insert(x, ".")
        if was_expanded:
            x += 1
        x += 1

    expanded_w = len(expanded_grid[0])
    return expanded_grid, expanded_w, expanded_h

grid, w, h = expand(grid, w, h)

def build_graph(grid, w, h):
    def adjacents_to(x, y):
        return [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
    graph = Graph()
    galaxies = []
    for y in range(h):
        for x in range(w):
            if grid[y][x] == "#":
                galaxies.append((x, y))

            for ax, ay, in adjacents_to(x, y):
                if ax < 0 or ax == w or ay < 0 or ay == h:
                    continue
                graph.add_edge((x, y), (ax, ay))
    return galaxies, graph

galaxies, graph = build_graph(grid, w, h)

checked = set()
tot = 0
res = all_pairs_shortest_path_length(graph)

shortest_paths = {}

for node, res2 in res:
    if node in galaxies:
        shortest_paths[node] = res2

for g1, shortest_paths in shortest_paths.items():
    for g2 in galaxies:
        if g1 == g2:
            continue
        if (g1, g2) in checked:
            continue
        tot += shortest_paths[g2]
        checked.add((g1, g2))
        checked.add((g2, g1))

print(f"Part 1: {tot}")

def expand2(grid, w, h):
    expanded_grid = []
    for y in range(h):
        expanded_grid.append(grid[y][:])
        if is_empty_row(grid, y, h):
            new_row = ["R" for x in grid[y][:]]
            expanded_grid.append(new_row)

    expanded_h = len(expanded_grid)

    x = 0
    while x < len(expanded_grid[0]):
        was_expanded = False
        if is_empty_column(expanded_grid, x, expanded_h):
            was_expanded = True
            for y in range(expanded_h):
                if expanded_grid[y][x] == "R":
                    expanded_grid[y].insert(x, "X")
                else:
                    expanded_grid[y].insert(x, "C")
        if was_expanded:
            x += 1
        x += 1

    expanded_w = len(expanded_grid[0])
    return expanded_grid, expanded_w, expanded_h

def build_graph2(grid, w, h):
    class Direction(Enum):
        UP = 0
        RIGHT = 1
        DOWN = 2
        LEFT = 3

    def adjacents_to(x, y):
        return [(x, y - 1, Direction.UP), (x - 1, y, Direction.LEFT), (x + 1, y, Direction.RIGHT), (x, y + 1, Direction.DOWN)]
    graph = Graph()
    galaxies = []
    for y in range(h):
        for x in range(w):
            if grid[y][x] == "#":
                galaxies.append((x, y))

            for ax, ay, direction in adjacents_to(x, y):
                if ax < 0 or ax == w or ay < 0 or ay == h:
                    continue

                weight = 1
                big_weight = 999999
                if direction in [Direction.RIGHT, Direction.LEFT] and grid[y][x] in [".", "#"] and grid[ay][ax] == "C":
                    weight = big_weight
                elif direction in [Direction.UP, Direction.DOWN] and grid[y][x] in [".", "#"] and grid[ay][ax] == "R":
                    weight = big_weight
                elif grid[ay][ax] == "X":
                    weight = big_weight + big_weight
                graph.add_edge((x, y), (ax, ay), weight=weight)
    return galaxies, graph

w = orig_w
h = orig_h

grid = [[lines[y][x] for x in range(w)] for y in range(h)]
grid, w, h = expand2(grid, w, h)
galaxies, graph = build_graph2(grid, w, h)

checked = set()
tot = 0
res = all_pairs_dijkstra_path_length(graph)

shortest_paths = {}

for node, res2 in res:
    if node in galaxies:
        shortest_paths[node] = res2

for g1, shortest_paths in shortest_paths.items():
    for g2 in galaxies:
        if g1 == g2:
            continue
        if (g1, g2) in checked:
            continue
        tot += shortest_paths[g2]
        checked.add((g1, g2))
        checked.add((g2, g1))

print(f"Part 2: {tot}")
