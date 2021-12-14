from pathlib import Path


def print_grid(g):
    for y in range(len(g)):
        for x in range(len(g[0])):
            print(g[y][x], end='')
        print()
    print()


lines = [x.strip() for x in Path("input.txt").open().readlines()]

w = 0
h = 0
coords = []
i = 0
for line in lines:
    if not line:
        break

    x = int(line.split(',')[0])
    y = int(line.split(',')[1])
    w = max(w, x + 1)
    h = max(h, y + 1)
    coords.append((x, y))
    i += 1

folds = []
for line in lines[i+1:]:
    res = line.split('fold along ')[1]
    folds.append((res.split('=')[0], int(res.split('=')[1])))

grid = [['.' for x in range(w)] for y in range(h)]
for x, y in coords:
    grid[y][x] = '#'


def split_grid(grid, axis, line):
    if axis == 'y':
        g1 = grid[:line]
        g2 = grid[line+1:]
    else:
        g1 = [['.' for x in range(line)] for y in range(len(grid))]
        g2 = [['.' for x in range(line)] for y in range(len(grid))]

        for y in range(len(grid)):
            for x in range(line):
                g1[y][x] = grid[y][x]
                g2[y][x] = grid[y][x+line+1]

    return g1, g2


def flip(grid, axis):
    g = [['.' for x in range(len(grid[0]))] for y in range(len(grid))]
    x = len(g[0]) - 1
    y = len(g) - 1
    if axis == 'y':
        for j in range(len(g)):
            for i in range(len(g[0])):
                g[y - j][i] = grid[j][i]
    else:
        for j in range(len(g)):
            for i in range(len(g[0])):
                g[j][x - i] = grid[j][i]

    return g


def merge(g1, g2, axis, line):
    g = [['.' for x in range(max(len(g1[0]), len(g2[0])))] for y in range(max(len(g1), len(g2)))]

    if axis == 'y':
        if len(g1) >= len(g2):
            for y in range(len(g1)):
                for x in range(len(g1[0])):
                    g[y][x] = g1[y][x]

            for y in range(len(g) - len(g2), len(g)):
                for x in range(len(g[0])):
                    if g2[y - (len(g) - len(g2))][x] == '#' or g[y][x] == '#':
                        g[y][x] = '#'
                    else:
                        g[y][x] = '.'
        else:
            for y in range(len(g2)):
                for x in range(len(g2[0])):
                    g[y][x] = g2[y][x]
            for y in range(len(g) - len(g1), len(g)):
                for x in range(len(g[0])):
                    if g1[y - (len(g) - len(g1))][x] == '#' or g[y][x] == '#':
                        g[y][x] = '#'
                    else:
                        g[y][x] = '.'
    else:
        if len(g1[0]) >= len(g2[0]):
            for y in range(len(g1)):
                for x in range(len(g1[0])):
                    g[y][x] = g1[y][x]
            for y in range(len(g)):
                for x in range(len(g[0]) - len(g2[0]), len(g[0])):
                    if g2[y][x - (len(g[0]) - len(g2[0]))] == '#' or g[y][x] == '#':
                        g[y][x] = '#'
                    else:
                        g[y][x] = '.'
        else:
            for y in range(len(g2)):
                for x in range(len(g2[0])):
                    g[y][x] = g2[y][x]
            for y in range(len(g)):
                for x in range(len(g[0]) - len(g1[0]), len(g[0])):
                    if g1[y][x - (len(g[0]) - len(g1[0]))] == '#' or g[y][x] == '#':
                        g[y][x] = '#'
                    else:
                        g[y][x] = '.'

    return g


res = []
part_1 = True
for axis, line in folds:
    g1, g2 = split_grid(grid, axis, line)
    r_g2 = flip(g2, axis)
    res = merge(g1, r_g2, axis, line)
    if part_1:
        sum = 0
        for y in range(len(res)):
            for x in range(len(res[0])):
                if res[y][x] == '#':
                    sum += 1
        print(f"Part 1: {sum}")
        part_1 = False

    grid = res

print("Part 2:")
print_grid(res)

