import ast
from pathlib import Path

lines = [x.strip() for x in Path("input.txt").open("r").readlines()]
sand = (500, 0)

w = 0
h = 0
rocks = []
for line in lines:
    rock = []
    for coord in line.split(" -> "):
        rock_coords = ast.literal_eval(coord)
        w = max(w, rock_coords[0] + 1 + 500)
        h = max(h, rock_coords[1] + 1)
        rock.append(rock_coords)
    rocks.append(rock)

grid = [["." for x in range(w)] for y in range(h)]


for y in range(h):
    for x in range(0, w):

        if (x, y) == sand:
            grid[y][x] = "+"

for rock in rocks:
    for i in range(len(rock) - 1):
        min_x = min(rock[i][0], rock[i+1][0])
        max_x = max(rock[i][0], rock[i+1][0])
        min_y = min(rock[i][1], rock[i+1][1])
        max_y = max(rock[i][1], rock[i+1][1])
        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                grid[y][x] = "#"


def print_grid():
    for y in range(h):
        for x in range(450, w):
            print(grid[y][x], end="")
        print()
    print()


def drop_sand(sx, sy):
    if sy + 1 == h:
        return False

    if grid[sy+1][sx-1] in "#O" and grid[sy+1][sx] in "#O" and grid[sy+1][sx+1] in "#O":
        if grid[sy][sx] == "+":
            return False
        grid[sy][sx] = "O"
        return True

    elif grid[sy+1][sx] in "#O" and grid[sy+1][sx-1] == ".":
        return drop_sand(sx - 1, sy + 1)
    elif grid[sy + 1][sx] in "#O" and grid[sy + 1][sx + 1] == ".":
        return drop_sand(sx + 1, sy + 1)

    elif grid[sy+1][sx] == ".":
        return drop_sand(sx, sy+1)


cnt = 0
while True:
    # print_grid()
    if drop_sand(*sand):
        cnt += 1
    else:
        break

print(f"Part 1: {cnt}")

w = 0
h = 0
rocks = []
for line in lines:
    rock = []
    for coord in line.split(" -> "):
        rock_coords = ast.literal_eval(coord)
        w = max(w, rock_coords[0] + 1 + 500)
        h = max(h, rock_coords[1] + 1 + 3)
        rock.append(rock_coords)
    rocks.append(rock)

grid = [["." for x in range(w)] for y in range(h)]


for y in range(h):
    for x in range(0, w):

        if (x, y) == sand:
            grid[y][x] = "+"

        if y == h - 1:
            grid[y][x] = "#"

        if y == h - 2:
            grid[y][x] = "#"

for rock in rocks:
    for i in range(len(rock) - 1):
        min_x = min(rock[i][0], rock[i+1][0])
        max_x = max(rock[i][0], rock[i+1][0])
        min_y = min(rock[i][1], rock[i+1][1])
        max_y = max(rock[i][1], rock[i+1][1])
        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                grid[y][x] = "#"

cnt = 0
while True:
    # print_grid()
    if drop_sand(*sand):
        cnt += 1
    else:
        break

print(f"Part 2: {cnt + 1}")
