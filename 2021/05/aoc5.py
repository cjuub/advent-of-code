from pathlib import Path

with Path("input.txt").open() as fp:
    lines = [x.strip() for x in fp.readlines()]


def print_grid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] != 0:
                print(grid[y][x], end='')
            else:
                print('.', end='')
        print()
    print()


ls = []
max_y = -1
min_y = 99999999999
max_x = -1
min_x = 99999999999
for line in lines:
    tmp = line.split(' -> ')
    src = (int(tmp[0].split(',')[0]), int(tmp[0].split(',')[1]))
    dst = (int(tmp[1].split(',')[0]), int(tmp[1].split(',')[1]))
    ls.append((src, dst))
    for x, y in [src, dst]:
        max_y = max(max_y, y)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        min_x = min(min_x, x)

h = max(max_x + 1, max_y + 1)
w = h
grid = [[0 for y in range(h)] for x in range(w)]

for l in ls:
    x1, y1 = l[0]
    x2, y2 = l[1]
    if y1 == y2:
        r = range(x1, x2 + 1) if x1 < x2 else range(x2, x1 + 1)
        for x in r:
            grid[y1][x] += 1
    if x1 == x2:
        r = range(y1, y2 + 1) if y1 < y2 else range(y2, y1 + 1)
        for y in r:
            grid[y][x1] += 1

cnt = 0
for y in range(h):
    for x in range(w):
        if grid[y][x] > 1:
            cnt += 1

print(f"Part 1: {cnt}")

grid = [[0 for y in range(h)] for x in range(w)]
for l in ls:
    x1, y1 = l[0]
    x2, y2 = l[1]
    if y1 == y2:
        r = range(x1, x2 + 1) if x1 < x2 else range(x2, x1 + 1)
        for x in r:
            grid[y1][x] += 1
    elif x1 == x2:
        r = range(y1, y2 + 1) if y1 < y2 else range(y2, y1 + 1)
        for y in r:
            grid[y][x1] += 1
    else:
        if x1 < x2 and y1 < y2:
            x = x1
            y = y1
            x_end = x2 + 1
            y_end = y2 + 1
            while x != x_end and y != y_end:
                grid[y][x] += 1
                x += 1
                y += 1
        elif x2 < x1 and y2 < y1:
            x = x1
            y = y1
            x_end = x2 - 1
            y_end = y2 - 1
            while x != x_end and y != y_end:
                grid[y][x] += 1
                x -= 1
                y -= 1
        elif x2 < x1 and y2 > y1:
            x = x1
            y = y1
            x_end = x2 - 1
            y_end = y2 + 1
            while x != x_end and y != y_end:
                grid[y][x] += 1
                x -= 1
                y += 1
        elif x2 > x1 and y2 < y1:
            x = x1
            y = y1
            x_end = x2 + 1
            y_end = y2 - 1
            while x != x_end and y != y_end:
                grid[y][x] += 1
                x += 1
                y -= 1
        else:
            raise Exception()

cnt = 0
for y in range(h):
    for x in range(w):
        if grid[y][x] > 1:
            cnt += 1

print(f"Part 2: {cnt}")
