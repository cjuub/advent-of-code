import sys
from enum import Enum
from pathlib import Path

lines = Path("input.txt").read_text().splitlines()

w = len(lines[0])
h = len(lines)
grid = [["." for x in [x for x in range(w)]] for y in range(h)]

start = None
for y in range(h):
    for x in range(w):
        grid[y][x] = lines[y][x]
        if grid[y][x] == "S":
            start = (x, y)

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

def adjacents_to(x, y):
    return [(x, y - 1, Direction.UP), (x - 1, y, Direction.LEFT), (x + 1, y, Direction.RIGHT), (x, y + 1, Direction.DOWN)]

def connects_to(curr, next, direction):
    if curr == "|":
        if direction == Direction.UP:
            return next in ["|", "7", "F", "S"]
        elif direction == Direction.DOWN:
            return next in ["|", "L", "J", "S"]
    elif curr == "-":
        if direction == Direction.RIGHT:
            return next in ["-", "J", "7", "S"]
        elif direction == Direction.LEFT:
            return next in ["-", "L", "F", "S"]
    elif curr == "L":
        if direction == Direction.UP:
            return next in ["|", "7", "F", "S"]
        elif direction == Direction.RIGHT:
            return next in ["-", "J", "7", "S"]
    elif curr == "J":
        if direction == Direction.UP:
            return next in ["|", "7", "F", "S"]
        elif direction == Direction.LEFT:
            return next in ["-", "L", "F", "S"]
    elif curr == "7":
        if direction == Direction.LEFT:
            return next in ["-", "L", "F", "S"]
        elif direction == Direction.DOWN:
            return next in ["|", "L", "J", "S"]
    elif curr == "F":
        if direction == Direction.RIGHT:
            return next in ["-", "J", "7", "S"]
        elif direction == Direction.DOWN:
            return next in ["|", "L", "J", "S"]
    elif curr == "S":
        if direction == Direction.UP:
            return next in ["|", "7", "F", "S"]
        elif direction == Direction.RIGHT:
            return next in ["-", "J", "7", "S"]
        elif direction == Direction.DOWN:
            return next in ["|", "L", "J", "S"]
        if direction == Direction.LEFT:
            return next in ["-", "L", "F", "S"]

    return False

def next_connection(g, curr_pos, prev_pos):
    x, y = curr_pos
    for ax, ay, direction in adjacents_to(*curr_pos):
        if (ax, ay) == prev_pos:
            continue
        try:
            if connects_to(g[y][x], g[ay][ax], direction):
                return (ax, ay, direction)
        except IndexError:
            continue
    raise Exception()

def find_loop(g, start_pos):
    loop = [start_pos]
    cx, cy, cd = next_connection(g, start_pos, None)
    prev_pos = start_pos
    while (cx, cy) != start_pos:
        loop.append((cx, cy, cd))
        tmp_pos = (cx, cy)
        cx, cy, cd = next_connection(g, (cx, cy), prev_pos)
        prev_pos = tmp_pos
    return loop

loop = find_loop(grid, start)
print(f"Part 1: {int(len(loop) / 2)}")


grid = [["." for x in [x for x in range(w)]] for y in range(h)]
start_replacement = "|"
start_replacement_dir = Direction.UP
loop[0] = (start[0], start[1], start_replacement_dir)

for y in range(h):
    for x in range(w):
        if (x, y) in [(tmp[0], tmp[1]) for tmp in loop]:
            if (x, y) == start:
                grid[y][x] = start_replacement
            else:
                grid[y][x] = lines[y][x]


def has_path_to_edge(g, prev_pos, curr_pos, outsiders, visited):
    x, y = curr_pos
    if y < 0 or y == h or x < 0 or x == w:
        outsiders.add(prev_pos)
        return True

    if curr_pos in outsiders:
        return True

    if g[y][x] != ".":
        return False

    for ax, ay, _ in adjacents_to(*curr_pos):
        if (ax, ay) in visited:
            continue

        visited.add((ax, ay))

        if (ax, ay) in outsiders or has_path_to_edge(g, curr_pos, (ax, ay), outsiders, visited):
            outsiders.add(prev_pos)
            return True

    return False

def find_outer_outsiders(g, curr_pos, outsiders):
    x, y = curr_pos
    if g[y][x] != ".":
        return

    if curr_pos in outsiders:
        return

    if has_path_to_edge(g, None, curr_pos, outsiders, set()):
        outsiders.add((x, y))


outsiders = set()
insiders = set()
start = None
outside_direction = None
for y in range(h):
    for x in range(w):
        find_outer_outsiders(grid, (x, y), outsiders)

        if start is None and (x, y) in [(tmp[0], tmp[1]) for tmp in loop]:
            for i, (ax, ay, direction) in enumerate(adjacents_to(x, y)):
                if (ax, ay) in outsiders:
                    start = (x, y)
                    outside_direction = direction

start_went = None

for x, y, went in loop:
    if (x, y) == start:
        start_went = went
        break

start_pos = (start[0], start[1], start_went)
i = loop.index(start_pos)
start_i = i
curr_outside = [Direction.LEFT]

prev_i = (start_i + len(loop) - 1) % len(loop)

while True:
    px, py, _ = loop[prev_i]
    x, y, went = loop[i]

    prev = grid[py][px]
    curr = grid[y][x]

    if curr == "|":
        if prev == "L":
            if Direction.LEFT in curr_outside:
                curr_outside = [Direction.LEFT]
            else:
                curr_outside = [Direction.RIGHT]
        elif prev == "J":
            if Direction.RIGHT in curr_outside:
                curr_outside = [Direction.RIGHT]
            else:
                curr_outside = [Direction.LEFT]
        elif prev == "7":
            if Direction.RIGHT in curr_outside:
                curr_outside = [Direction.RIGHT]
            else:
                curr_outside = [Direction.LEFT]
        elif prev == "F":
            if Direction.LEFT in curr_outside:
                curr_outside = [Direction.LEFT]
            else:
                curr_outside = [Direction.RIGHT]
        elif prev == "|":
            pass
        else:
            assert False, (prev, curr)
    elif curr == "-":
        if prev == "L":
            if Direction.DOWN in curr_outside:
                curr_outside = [Direction.DOWN]
            else:
                curr_outside = [Direction.UP]
        elif prev == "J":
            if Direction.DOWN in curr_outside:
                curr_outside = [Direction.DOWN]
            else:
                curr_outside = [Direction.UP]
        elif prev == "7":
            if Direction.RIGHT in curr_outside:
                curr_outside = [Direction.UP]
            else:
                curr_outside = [Direction.DOWN]
        elif prev == "F":
            if Direction.LEFT in curr_outside:
                curr_outside = [Direction.UP]
            else:
                curr_outside = [Direction.DOWN]
        elif prev == "-":
            pass
        else:
            assert False, (prev, curr, (x, y))
    elif curr == "L":
        if prev == "-":
            if Direction.DOWN in curr_outside:
                curr_outside = [Direction.DOWN, Direction.LEFT]
            else:
                curr_outside = [Direction.UP, Direction.RIGHT]
        elif prev == "|":
            if Direction.LEFT in curr_outside:
                curr_outside = [Direction.DOWN, Direction.LEFT]
            else:
                curr_outside = [Direction.UP, Direction.RIGHT]
        elif prev == "J":
            if Direction.DOWN in curr_outside:
                curr_outside = [Direction.DOWN, Direction.LEFT]
            else:
                curr_outside = [Direction.UP, Direction.RIGHT]
        elif prev == "7":
            if Direction.RIGHT in curr_outside:
                curr_outside = [Direction.UP, Direction.RIGHT]
            else:
                curr_outside = [Direction.DOWN, Direction.LEFT]
        elif prev == "F":
            if Direction.LEFT in curr_outside:
                curr_outside = [Direction.LEFT, Direction.DOWN]
            else:
                curr_outside = [Direction.UP, Direction.RIGHT]
        else:
            assert False
    elif curr == "J":
        if prev == "-":
            if Direction.DOWN in curr_outside:
                curr_outside = [Direction.DOWN, Direction.RIGHT]
            else:
                curr_outside = [Direction.UP, Direction.LEFT]
        elif prev == "|":
            if Direction.RIGHT in curr_outside:
                curr_outside = [Direction.DOWN, Direction.RIGHT]
            else:
                curr_outside = [Direction.UP, Direction.LEFT]
        elif prev == "L":
            if Direction.LEFT in curr_outside:
                curr_outside = [Direction.DOWN, Direction.RIGHT]
            else:
                curr_outside = [Direction.UP, Direction.LEFT]
        elif prev == "7":
            if Direction.RIGHT in curr_outside:
                curr_outside = [Direction.DOWN, Direction.RIGHT]
            else:
                curr_outside = [Direction.UP, Direction.LEFT]
        elif prev == "F":
            if Direction.LEFT in curr_outside:
                curr_outside = [Direction.UP, Direction.LEFT]
            else:
                curr_outside = [Direction.DOWN, Direction.RIGHT]
        else:
            assert False
    elif curr == "7":
        if prev == "-":
            if Direction.UP in curr_outside:
                curr_outside = [Direction.UP, Direction.RIGHT]
            else:
                curr_outside = [Direction.DOWN, Direction.LEFT]
        elif prev == "|":
            if Direction.RIGHT in curr_outside:
                curr_outside = [Direction.UP, Direction.RIGHT]
            else:
                curr_outside = [Direction.DOWN, Direction.LEFT]
        elif prev == "L":
            if Direction.LEFT in curr_outside:
                curr_outside = [Direction.DOWN, Direction.LEFT]
            else:
                curr_outside = [Direction.UP, Direction.RIGHT]
        elif prev == "J":
            if Direction.RIGHT in curr_outside:
                curr_outside = [Direction.UP, Direction.RIGHT]
            else:
                curr_outside = [Direction.DOWN, Direction.LEFT]
        elif prev == "F":
            if Direction.LEFT in curr_outside:
                curr_outside = [Direction.UP, Direction.RIGHT]
            else:
                curr_outside = [Direction.DOWN, Direction.LEFT]
        else:
            assert False
    elif curr == "F":
        if prev == "-":
            if Direction.UP in curr_outside:
                curr_outside = [Direction.UP, Direction.LEFT]
            else:
                curr_outside = [Direction.DOWN, Direction.RIGHT]
        elif prev == "|":
            if Direction.LEFT in curr_outside:
                curr_outside = [Direction.UP, Direction.LEFT]
            else:
                curr_outside = [Direction.DOWN, Direction.RIGHT]
        elif prev == "L":
            if Direction.LEFT in curr_outside:
                curr_outside = [Direction.UP, Direction.LEFT]
            else:
                curr_outside = [Direction.DOWN, Direction.RIGHT]
        elif prev == "J":
            if Direction.RIGHT in curr_outside:
                curr_outside = [Direction.DOWN, Direction.RIGHT]
            else:
                curr_outside = [Direction.UP, Direction.LEFT]
        elif prev == "7":
            if Direction.RIGHT in curr_outside:
                curr_outside = [Direction.UP, Direction.LEFT]
            else:
                curr_outside = [Direction.DOWN, Direction.RIGHT]
        else:
            assert False
    else:
        assert False

    for ax, ay, direction in adjacents_to(x, y):
        if direction in curr_outside:
            continue

        if grid[ay][ax] == "." and (ax, ay) not in outsiders:
            insiders.add((ax, ay))

    prev_i = i
    i = (i + 1) % len(loop)
    if i == start_i:
        break

def has_path_to_inside(g, prev_pos, curr_pos, insiders, visited):
    x, y = curr_pos
    if curr_pos in insiders:
        return True

    if g[y][x] != ".":
        return False

    for ax, ay, _ in adjacents_to(*curr_pos):
        if (ax, ay) in visited:
            continue

        visited.add((ax, ay))

        if (ax, ay) in outsiders or has_path_to_inside(g, curr_pos, (ax, ay), insiders, visited):
            insiders.add(prev_pos)
            return True

    return False

for y in range(h):
    for x in range(w):

        if (x, y) in outsiders:
            grid[y][x] = "O"

        if grid[y][x] == ".":
            if has_path_to_inside(grid, None, (x, y), insiders, set()):
                insiders.add((x, y))

        if (x, y) in insiders:
            grid[y][x] = "I"

tot = 0
for y in range(h):
    for x in range(w):
        if grid[y][x] == "I":
            tot += 1

print(f"Part 2: {tot}")

