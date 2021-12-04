from pathlib import Path

with Path('input.txt').open() as fp:
    lines = fp.readlines()

vals = lines[0].split(',')
vals = [int(x) for x in vals]

w = 5
grids = []
rows = []
for line in lines[2:]:
    line = line.strip()
    if line:
        line = line.replace('  ', ' ')
        column = line.split(' ')
        column = [(int(x), False) for x in column]
        rows.append(column)
    else:
        grids.append(rows)
        rows = []
grids.append(rows)


def print_grid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x][1]:
                print(grid[y][x][0], end=' ')
            else:
                print('..', end=' ')
        print()
    print()


last = None
first = True
while vals:
    val = vals.pop(0)
    for grid in grids:
        for y in range(w):
            for x in range(w):
                if val == grid[y][x][0]:
                    grid[y][x] = (grid[y][x][0], True)

    for i, grid in enumerate(grids):
        bingo = False
        for x in range(w):
            y_bingo = True
            for y in range(w):
                if not grid[y][x][1]:
                    y_bingo = False
            if y_bingo:
                bingo = True

        for y in range(w):
            x_bingo = True
            for x in range(w):
                if not grid[y][x][1]:
                    x_bingo = False
            if x_bingo:
                bingo = True

        if bingo:
            sum = 0
            for y in range(w):
                for x in range(w):
                    if not grid[y][x][1]:
                        sum += grid[y][x][0]
            if first:
                print(f"Part 1: {sum * val}")
                first = False

            last = sum * val
            del grids[i]

print(f"Part 2: {last}")
