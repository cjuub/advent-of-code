#!/usr/bin/env python3

with open('input.txt') as fp:
    lines2 = fp.readlines()

lines = []
for line in lines2:
    line = line.strip()
    lines.append(line)
    
init_grid = [['.' for y in range(len(lines))] for x in range(len(lines[0]))]


def copy_grid(grid):
    copy = [['' for y in range(len(grid[0]))] for x in range(len(grid))]
    for y in range(len(grid[0])):
        for x in range(len(grid)):
            copy[x][y] = grid[x][y]

    return copy


def print_grid(grid):
    for y in range(len(grid[0])):
        for x in range(len(grid)):
            print(grid[x][y], end='')
        print()


def expand_grid(grid):
    new_grid = [['.' for y in range(len(grid) + 2)] for x in range(len(grid[0]) + 2)]

    for y in range(1, len(grid[0]) + 1):
        for x in range(1, len(grid) + 1):
            new_grid[x][y] = grid[x-1][y-1]
            
    return new_grid


def neighbors(layers, x1, y1, z1):
    ns = []
    nbr_active = 0
    for z in [z1 - 1, z1, z1 + 1]:
        for y in [y1 - 1, y1, y1 + 1]:
            for x in [x1 - 1, x1, x1 + 1]:
                if (x, y, z) == (x1, y1, z1):
                    continue
                try:
                    ns.append((x, y, z, layers[z][x][y]))
                except:
                    continue
                if layers[z][x][y] == '#':
                    nbr_active += 1
                
    return ns, nbr_active


for y in range(len(lines)):
    for x in range(len(lines[0])):
        init_grid[x][y] = lines[y][x]

empty_grid = copy_grid(init_grid)
for y in range(len(lines)):
    for x in range(len(lines[0])):
        empty_grid[x][y] = '.'
        

max_depth = 20
layers = []
for i in range(max_depth):
    layers.append(copy_grid(empty_grid))

layers[int(max_depth / 2)] = copy_grid(init_grid)

cnt = 0
while True:
    for z in range(0, len(layers)):
        layers[z] = expand_grid(layers[z])

    new_layers = []
    new_layers.append(layers[0])
    for z in range(1, len(layers) - 1):
        new = copy_grid(layers[z])

        l = layers[z]
        for y in range(len(l[0])):
            for x in range(len(l)):
                ns, nbr_active = neighbors(layers, x, y, z)
                if l[x][y] == '#':
                    if not (nbr_active == 2 or nbr_active == 3):
                        new[x][y] = '.'
                else:
                    if nbr_active == 3:
                        new[x][y] = '#'

        new_layers.append(copy_grid(new))
    new_layers.append(layers[-1])

    layers = new_layers

    if cnt == 5:
        break

    cnt += 1
    

res = 0
for l in layers:
    for y in range(len(l[0])):
        for x in range(len(l)):
            if l[x][y] == '#':
                res += 1

print('Part 1: {}'.format(res))

vals = {}
min_x = 0
max_x = 1
min_y = 0
max_y = 1
min_z = 0
max_z = 1
min_w = 0
max_w = 1
for y in range(len(lines)):
    for x in range(len(lines[0])):
        vals[(x, y, 0, 0)] = lines[y][x]
        max_y = max(y + 1, max_y)
        min_y = min(y, min_y)
        max_x = max(x + 1, max_x)
        min_x = min(x, min_x)


def neighbors2(vals, x1, y1, z1, w1):
    nbr_active = 0

    for w in [w1 - 1, w1, w1 + 1]:
        for z in [z1 - 1, z1, z1 + 1]:
            for y in [y1 - 1, y1, y1 + 1]:
                for x in [x1 - 1, x1, x1 + 1]:
                    if (x, y, z, w) == (x1, y1, z1, w1):
                        continue
                    try:
                        a = vals[x, y, z, w]
                    except:
                        continue
                    if vals[(x, y, z, w)] == '#':
                        nbr_active += 1

    return nbr_active


def expand(vals):
    global max_x, max_y, max_z, max_w, min_x, min_y, min_z, min_w

    for w in range(min_w - 1, max_w + 1):
        for z in range(min_z - 1, max_z + 1):
            for y in range(min_y - 1, max_y + 1):
                for x in range(min_x - 1, max_x + 1):
                    if (x, y, z, w) not in vals.keys():
                        vals[(x, y, z, w)] = '.'

    max_x = max_x + 1
    min_x = min_x - 1
    max_y = max_y + 1
    min_y = min_y - 1
    max_z = max_z + 1
    min_z = min_z - 1
    max_w = max_w + 1
    min_w = min_w - 1


depth = 0
cnt = 0
while cnt < 6:
    new = {}
    expand(vals)
    for w in range(min_w, max_w):
        for z in range(min_z, max_z):
            for y in range(min_y, max_y):
                for x in range(min_x, max_x):
                    nbr_active = neighbors2(vals, x, y, z, w)
                    if vals[(x, y, z, w)] == '#':
                        if not (nbr_active == 2 or nbr_active == 3):
                            new[(x, y, z, w)] = '.'
                    else:
                        if nbr_active == 3:
                            new[(x, y, z, w)] = '#'
                        
    for coord, val in new.items():
        vals[coord] = val

    cnt += 1

res = 0
for coord, val in vals.items():
    if val == '#':
        res += 1

print('Part 2: {}'.format(res))
