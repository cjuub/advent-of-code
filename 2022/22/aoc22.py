import sys
from pathlib import Path


def print_grid(grid):
    for y in range(h):
        for x in range(w):
            print(grid[y][x], end="")
        print()
    print()


def parse_path(curr, path_str, build, path):
    if curr == len(path_str):
        path.append(int(build))
        return path

    if path_str[curr] in "LR":
        path.append(int(build))
        path.append(path_str[curr])
        return parse_path(curr + 1, path_str, "", path)
    else:
        return parse_path(curr + 1, path_str, build + path_str[curr], path)


RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

lines = [x[:-1] for x in Path("input.txt").open("r").readlines()]

path_str = lines[-1]
lines = lines[:-2]

h = len(lines)
w = 0
for line in lines:
    w = max(len(line), w)

g = [[" " for x in range(w)] for y in range(h)]

for y in range(h):
    for x in range(w):
        try:
            g[y][x] = lines[y][x]
        except:
            g[y][x] = " "

sys.setrecursionlimit(20000)
path = parse_path(0, path_str, "", [])
pos = (g[0].index("."), 0)
heading = RIGHT

# print_grid(g)
# print(path)
# print(pos)


def get_wrap_pos(x, y):
    if heading == RIGHT:
        for i in range(w):
            if g[y][i] != " ":
                return i, y
    elif heading == DOWN:
        for i in range(h):
            if g[i][x] != " ":
                return x, i
    elif heading == LEFT:
        for i in range(w-1, 0, -1):
            if g[y][i] != " ":
                return i, y
    else:
        for i in range(h-1, 0, -1):
            if g[i][x] != " ":
                return x, i


def get_next_pos():
    if heading == RIGHT:
        new_pos = pos[0] + 1, pos[1]
    elif heading == DOWN:
        new_pos = pos[0], pos[1] + 1
    elif heading == LEFT:
        new_pos = pos[0] - 1, pos[1]
    else:
        new_pos = pos[0], pos[1] - 1

    x, y = new_pos
    if x == w or y == h or g[y][x] == " ":
        new_pos = get_wrap_pos(x, y)

    return new_pos


def get_next_heading(turn):
    if turn == "R":
        if heading == RIGHT:
            return DOWN
        elif heading == DOWN:
            return LEFT
        elif heading == LEFT:
            return UP
        else:
            return RIGHT
    else:
        if heading == RIGHT:
            return UP
        elif heading == DOWN:
            return RIGHT
        elif heading == LEFT:
            return DOWN
        else:
            return LEFT


for p in path:
    if isinstance(p, int):
        for i in range(p):
            x, y = get_next_pos()
            if g[y][x] == "#":
                break
            pos = (x, y)
    else:
        heading = get_next_heading(p)


print(f"Part 1: {1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + heading}")


def get_curr_side(x, y):
    for s, (sx, sy) in side_bounds.items():
        if x in range(sx, sx + side_size) and y in range(sy, sy + side_size):
            return s
    assert False


def get_next_pos2():
    global heading
    if heading == RIGHT:
        new_pos = pos[0] + 1, pos[1]
    elif heading == DOWN:
        new_pos = pos[0], pos[1] + 1
    elif heading == LEFT:
        new_pos = pos[0] - 1, pos[1]
    else:
        new_pos = pos[0], pos[1] - 1

    x, y = new_pos
    if x == w or y == h or g[y][x] == " ":
        curr_s = get_curr_side(*pos)
        target_s, target_heading = side_heading_map[(curr_s, heading)]
        new_pos = side_position_map[curr_s][target_s][(x, y)]
        heading = side_heading_map[(curr_s, heading)][1]

    return new_pos


SIDE_FRONT = 0
SIDE_TOP = 1
SIDE_LEFT = 2
SIDE_BACK = 3
SIDE_BOTTOM = 4
SIDE_RIGHT = 5

side_position_map = {}
side_position_map[SIDE_FRONT] = {}
side_position_map[SIDE_FRONT][SIDE_RIGHT] = {}
side_position_map[SIDE_FRONT][SIDE_LEFT] = {}

side_position_map[SIDE_TOP] = {}
side_position_map[SIDE_TOP][SIDE_RIGHT] = {}
side_position_map[SIDE_TOP][SIDE_LEFT] = {}
side_position_map[SIDE_TOP][SIDE_BACK] = {}

side_position_map[SIDE_LEFT] = {}
side_position_map[SIDE_LEFT][SIDE_TOP] = {}
side_position_map[SIDE_LEFT][SIDE_BOTTOM] = {}
side_position_map[SIDE_LEFT][SIDE_FRONT] = {}

side_position_map[SIDE_BACK] = {}
side_position_map[SIDE_BACK][SIDE_TOP] = {}
side_position_map[SIDE_BACK][SIDE_RIGHT] = {}
side_position_map[SIDE_BACK][SIDE_BOTTOM] = {}

side_position_map[SIDE_BOTTOM] = {}
side_position_map[SIDE_BOTTOM][SIDE_LEFT] = {}
side_position_map[SIDE_BOTTOM][SIDE_BACK] = {}
side_position_map[SIDE_BOTTOM][SIDE_RIGHT] = {}

side_position_map[SIDE_RIGHT] = {}
side_position_map[SIDE_RIGHT][SIDE_FRONT] = {}
side_position_map[SIDE_RIGHT][SIDE_TOP] = {}
side_position_map[SIDE_RIGHT][SIDE_BACK] = {}
side_position_map[SIDE_RIGHT][SIDE_BOTTOM] = {}

# EXAMPLE
# side_size = 4
# side_bounds = {
#     SIDE_FRONT: (8, 4),
#     SIDE_TOP: (8, 0),
#     SIDE_LEFT: (4, 4),
#     SIDE_BACK: (0, 4),
#     SIDE_BOTTOM: (8, 8),
#     SIDE_RIGHT: (12, 8),
# }
#
# side_heading_map = {
#     (SIDE_FRONT, RIGHT): (SIDE_RIGHT, DOWN),
#     (SIDE_FRONT, DOWN): (SIDE_BOTTOM, DOWN),
#     (SIDE_FRONT, LEFT): (SIDE_LEFT, LEFT),
#     (SIDE_FRONT, UP): (SIDE_TOP, UP),
#
#     (SIDE_TOP, RIGHT): (SIDE_RIGHT, LEFT),
#     (SIDE_TOP, DOWN): (SIDE_FRONT, DOWN),
#     (SIDE_TOP, LEFT): (SIDE_LEFT, DOWN),
#     (SIDE_TOP, UP): (SIDE_BACK, DOWN),
#
#     (SIDE_LEFT, RIGHT): (SIDE_FRONT, RIGHT),
#     (SIDE_LEFT, DOWN): (SIDE_BOTTOM, RIGHT),
#     (SIDE_LEFT, LEFT): (SIDE_BACK, LEFT),
#     (SIDE_LEFT, UP): (SIDE_TOP, RIGHT),
#
#     (SIDE_BACK, RIGHT): (SIDE_FRONT, RIGHT),
#     (SIDE_BACK, DOWN): (SIDE_BOTTOM, UP),
#     (SIDE_BACK, LEFT): (SIDE_RIGHT, UP),
#     (SIDE_BACK, UP): (SIDE_TOP, DOWN),
#
#     (SIDE_BOTTOM, RIGHT): (SIDE_RIGHT, RIGHT),
#     (SIDE_BOTTOM, DOWN): (SIDE_BACK, UP),
#     (SIDE_BOTTOM, LEFT): (SIDE_LEFT, UP),
#     (SIDE_BOTTOM, UP): (SIDE_FRONT, UP),
#
#     (SIDE_RIGHT, RIGHT): (SIDE_TOP, LEFT),
#     (SIDE_RIGHT, DOWN): (SIDE_BACK, RIGHT),
#     (SIDE_RIGHT, LEFT): (SIDE_BOTTOM, LEFT),
#     (SIDE_RIGHT, UP): (SIDE_FRONT, LEFT),
# }
#
#
# for i in range(side_size):
#     sx, sy = side_bounds[SIDE_FRONT]
#     target_sx, target_sy = side_bounds[SIDE_RIGHT]
#     side_position_map[SIDE_FRONT][SIDE_RIGHT][(sx + side_size, sy + i)] = (target_sx + side_size - 1 - i, target_sy)
#
#     sx, sy = side_bounds[SIDE_TOP]
#     target_sx, target_sy = side_bounds[SIDE_RIGHT]
#     side_position_map[SIDE_TOP][SIDE_RIGHT][(sx + side_size, sy + i)] = (target_sx + side_size - i - 1, target_sy)
#     target_sx, target_sy = side_bounds[SIDE_LEFT]
#     side_position_map[SIDE_TOP][SIDE_LEFT][(sx - 1, sy + i)] = (target_sx + i, target_sy)
#     target_sx, target_sy = side_bounds[SIDE_BACK]
#     side_position_map[SIDE_TOP][SIDE_BACK][(sx + i, sy - 1)] = (target_sx + side_size - i - 1, target_sy)
#
#     sx, sy = side_bounds[SIDE_LEFT]
#     target_sx, target_sy = side_bounds[SIDE_TOP]
#     side_position_map[SIDE_LEFT][SIDE_TOP][(sx + i, sy - 1)] = (target_sx, target_sy + i)
#     target_sx, target_sy = side_bounds[SIDE_BOTTOM]
#     side_position_map[SIDE_LEFT][SIDE_BOTTOM][(sx + i, sy + side_size)] = (target_sx, target_sy + side_size - 1 - i)
#
#     sx, sy = side_bounds[SIDE_BACK]
#     target_sx, target_sy = side_bounds[SIDE_TOP]
#     side_position_map[SIDE_BACK][SIDE_TOP][(sx + i, sy - 1)] = (target_sx + side_size - 1 - i, target_sy)
#     target_sx, target_sy = side_bounds[SIDE_RIGHT]
#     side_position_map[SIDE_BACK][SIDE_RIGHT][(sx - 1, sy + i)] = (target_sx + side_size - 1 - i, target_sy + side_size - 1)
#     target_sx, target_sy = side_bounds[SIDE_BOTTOM]
#     side_position_map[SIDE_BACK][SIDE_BOTTOM][(sx + i, sy + side_size)] = (target_sx + side_size - 1 - i, target_sy + side_size - 1)
#
#     sx, sy = side_bounds[SIDE_BOTTOM]
#     target_sx, target_sy = side_bounds[SIDE_LEFT]
#     side_position_map[SIDE_BOTTOM][SIDE_LEFT][(sx - 1, sy + i)] = (target_sx + side_size - 1 - i, target_sy + side_size - 1)
#     target_sx, target_sy = side_bounds[SIDE_BACK]
#     side_position_map[SIDE_BOTTOM][SIDE_BACK][(sx + i, sy + side_size)] = (target_sx + side_size - 1 - i, target_sy + side_size - 1)
#
#     sx, sy = side_bounds[SIDE_RIGHT]
#     target_sx, target_sy = side_bounds[SIDE_LEFT]
#     side_position_map[SIDE_RIGHT][SIDE_FRONT][(sx + i, sy - 1)] = (target_sx + side_size - 1, target_sy + i)
#     target_sx, target_sy = side_bounds[SIDE_TOP]
#     side_position_map[SIDE_RIGHT][SIDE_TOP][(sx + side_size, sy + i)] = (target_sx + side_size - 1, target_sy + side_size - 1 - i)
#     target_sx, target_sy = side_bounds[SIDE_BACK]
#     side_position_map[SIDE_RIGHT][SIDE_BACK][(sx + i, sy + side_size)] = (target_sx + side_size - 1, target_sy + side_size - 1 - i)

# INPUT
side_size = 50
side_bounds = {
    SIDE_FRONT: (50, 50),
    SIDE_TOP: (50, 0),
    SIDE_LEFT: (0, 100),
    SIDE_BACK: (0, 150),
    SIDE_BOTTOM: (50, 100),
    SIDE_RIGHT: (100, 0),
}

side_heading_map = {
    (SIDE_FRONT, RIGHT): (SIDE_RIGHT, UP),
    (SIDE_FRONT, DOWN): (SIDE_BOTTOM, DOWN),
    (SIDE_FRONT, LEFT): (SIDE_LEFT, DOWN),
    (SIDE_FRONT, UP): (SIDE_TOP, UP),

    (SIDE_TOP, RIGHT): (SIDE_RIGHT, RIGHT),
    (SIDE_TOP, DOWN): (SIDE_FRONT, DOWN),
    (SIDE_TOP, LEFT): (SIDE_LEFT, RIGHT),
    (SIDE_TOP, UP): (SIDE_BACK, RIGHT),

    (SIDE_LEFT, RIGHT): (SIDE_BOTTOM, RIGHT),
    (SIDE_LEFT, DOWN): (SIDE_BACK, DOWN),
    (SIDE_LEFT, LEFT): (SIDE_TOP, RIGHT),
    (SIDE_LEFT, UP): (SIDE_FRONT, RIGHT),

    (SIDE_BACK, RIGHT): (SIDE_BOTTOM, UP),
    (SIDE_BACK, DOWN): (SIDE_RIGHT, DOWN),
    (SIDE_BACK, LEFT): (SIDE_TOP, DOWN),
    (SIDE_BACK, UP): (SIDE_LEFT, UP),

    (SIDE_BOTTOM, RIGHT): (SIDE_RIGHT, LEFT),
    (SIDE_BOTTOM, DOWN): (SIDE_BACK, LEFT),
    (SIDE_BOTTOM, LEFT): (SIDE_LEFT, LEFT),
    (SIDE_BOTTOM, UP): (SIDE_FRONT, UP),

    (SIDE_RIGHT, RIGHT): (SIDE_BOTTOM, LEFT),
    (SIDE_RIGHT, DOWN): (SIDE_FRONT, LEFT),
    (SIDE_RIGHT, LEFT): (SIDE_TOP, LEFT),
    (SIDE_RIGHT, UP): (SIDE_BACK, UP),
}


for i in range(side_size):
    sx, sy = side_bounds[SIDE_FRONT]
    target_sx, target_sy = side_bounds[SIDE_RIGHT]
    side_position_map[SIDE_FRONT][SIDE_RIGHT][(sx + side_size, sy + i)] = (target_sx + i, target_sy + side_size - 1)
    target_sx, target_sy = side_bounds[SIDE_LEFT]
    side_position_map[SIDE_FRONT][SIDE_LEFT][(sx - 1, sy + i)] = (target_sx + i, target_sy)

    sx, sy = side_bounds[SIDE_TOP]
    target_sx, target_sy = side_bounds[SIDE_LEFT]
    side_position_map[SIDE_TOP][SIDE_LEFT][(sx - 1, sy + i)] = (target_sx, target_sy + side_size - 1 - i)
    target_sx, target_sy = side_bounds[SIDE_BACK]
    side_position_map[SIDE_TOP][SIDE_BACK][(sx + i, sy - 1)] = (target_sx, target_sy + i)

    sx, sy = side_bounds[SIDE_LEFT]
    target_sx, target_sy = side_bounds[SIDE_FRONT]
    side_position_map[SIDE_LEFT][SIDE_FRONT][(sx + i, sy - 1)] = (target_sx, target_sy + i)
    target_sx, target_sy = side_bounds[SIDE_TOP]
    side_position_map[SIDE_LEFT][SIDE_TOP][(sx - 1, sy + i)] = (target_sx, target_sy + side_size - 1 - i)

    sx, sy = side_bounds[SIDE_BACK]
    target_sx, target_sy = side_bounds[SIDE_TOP]
    side_position_map[SIDE_BACK][SIDE_TOP][(sx - 1, sy + i)] = (target_sx + i, target_sy)
    target_sx, target_sy = side_bounds[SIDE_RIGHT]
    side_position_map[SIDE_BACK][SIDE_RIGHT][(sx + i, sy + side_size)] = (target_sx + i, target_sy)
    target_sx, target_sy = side_bounds[SIDE_BOTTOM]
    side_position_map[SIDE_BACK][SIDE_BOTTOM][(sx + side_size, sy + i)] = (target_sx + i, target_sy + side_size - 1)

    sx, sy = side_bounds[SIDE_BOTTOM]
    target_sx, target_sy = side_bounds[SIDE_RIGHT]
    side_position_map[SIDE_BOTTOM][SIDE_RIGHT][(sx + side_size, sy + i)] = (target_sx + side_size - 1, target_sy + side_size - 1 - i)
    target_sx, target_sy = side_bounds[SIDE_BACK]
    side_position_map[SIDE_BOTTOM][SIDE_BACK][(sx + i, sy + side_size)] = (target_sx + side_size - 1, target_sy + i)

    sx, sy = side_bounds[SIDE_RIGHT]
    target_sx, target_sy = side_bounds[SIDE_BACK]
    side_position_map[SIDE_RIGHT][SIDE_BACK][(sx + i, sy - 1)] = (target_sx + i, target_sy + side_size - 1)
    target_sx, target_sy = side_bounds[SIDE_BOTTOM]
    side_position_map[SIDE_RIGHT][SIDE_BOTTOM][(sx + side_size, sy + i)] = (target_sx + side_size - 1, target_sy + side_size - 1 - i)
    target_sx, target_sy = side_bounds[SIDE_FRONT]
    side_position_map[SIDE_RIGHT][SIDE_FRONT][(sx + i, sy + side_size)] = (target_sx + side_size - 1, target_sy + i)

pos = (g[0].index("."), 0)
heading = RIGHT
for p in path:
    if isinstance(p, int):
        for i in range(p):
            h_before = heading
            x, y = get_next_pos2()
            if g[y][x] == "#":
                if h_before != heading:
                    heading = h_before
                break
            pos = (x, y)
    else:
        heading = get_next_heading(p)


print(f"Part 2: {1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + heading}")
