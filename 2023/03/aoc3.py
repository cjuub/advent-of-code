import numpy
from pathlib import Path


def adjacents(x, y):
    return [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]

lines = Path("input.txt").read_text().splitlines()
w = len(lines[0])
h = len(lines)
grid = [["." for x in range(w)] for y in range(h)]

for y in range(h):
    for x in range(w):
        grid[y][x] = lines[y][x]

vals = []
y = 0
while y < h:
    x = 0
    while x < w:
        has_symbol = False
        if grid[y][x].isnumeric():
            for ax, ay in adjacents(x, y):
                try:
                    if not grid[ay][ax].isnumeric() and not grid[ay][ax] == ".":
                        has_symbol = True
                        break
                except:
                    pass

        if has_symbol:
            val = grid[y][x]

            next_x = x - 1
            while next_x >= 0 and grid[y][next_x].isnumeric():
                val = grid[y][next_x] + val
                next_x -= 1

            next_x = x + 1
            while next_x < w and grid[y][next_x].isnumeric():
                val += grid[y][next_x]
                next_x += 1

            vals.append(int(val))
            x = next_x - 1
        x += 1
    y += 1

print(f"Part 1: {sum(vals)}")


gears = {}
vals = []
y = 0
while y < h:
    x = 0
    while x < w:
        has_symbol = False
        gear_x = 0
        gear_y = 0
        if grid[y][x].isnumeric():
            for ax, ay in adjacents(x, y):
                try:
                    if not grid[ay][ax].isnumeric() and grid[ay][ax] == "*":
                        gear_x = ax
                        gear_y = ay
                        has_symbol = True
                        break
                except:
                    pass

        if has_symbol:
            val = grid[y][x]

            next_x = x - 1
            while next_x >= 0 and grid[y][next_x].isnumeric():
                val = grid[y][next_x] + val
                next_x -= 1

            next_x = x + 1
            while next_x < w and grid[y][next_x].isnumeric():
                val += grid[y][next_x]
                next_x += 1

            if (gear_x, gear_y) not in gears:
                gears[(gear_x, gear_y)] = []
            gears[(gear_x, gear_y)].append(int(val))
            x = next_x - 1
        x += 1
    y += 1

sum = 0
for gear, vals in gears.items():
    if len(vals) > 1:
        sum += numpy.prod(vals)

print(f"Part 2: {sum}")

