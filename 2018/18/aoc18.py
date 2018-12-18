#!/usr/bin/env python3

input = []
with open('input.txt') as fp:
    for line in fp:
        input.append(list(line.strip()))


grid = [['' for y in range(len(input))] for x in range(len(input[0]))]
for y in range(len(input)):
    for x in range(len(input[0])):
        grid[x][y] = input[y][x]


def print_grid():
    for y in range(len(input)):
        for x in range(len(input[0])):
            print(grid[x][y], end='')
        print()

def copy_grid(grid):
    copy = [['' for y in range(len(grid[0]))] for x in range(len(grid))]
    for y in range(len(grid[0])):
        for x in range(len(grid)):
            copy[x][y] = grid[x][y]

    return copy

def adjacents(x, y):
    return [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]


print_grid()
print()
vals = []
# for min in range(10): # part 1
for min in range(10000): # part 2
    curr_grid = copy_grid(grid)
    for y in range(len(input)):
        for x in range(len(input[0])):
            adjs = adjacents(x, y)
            nbr_trees = 0
            nbr_lumb = 0
            for adj in adjs:
                if adj[0] < 0 or adj[0] > len(grid):
                    continue
                if adj[1] < 0 or adj[1] > len(grid):
                    continue

                try:
                    if grid[adj[0]][adj[1]] == '|':
                        nbr_trees += 1
                    elif grid[adj[0]][adj[1]] == '#':
                        nbr_lumb += 1
                except IndexError:
                    pass

            if grid[x][y] == '|' and nbr_lumb >= 3:
                curr_grid[x][y] = '#'
            elif grid[x][y] == '.' and nbr_trees >= 3:
                curr_grid[x][y] = '|'
            elif grid[x][y] == '#' and nbr_lumb >= 1 and nbr_trees >= 1:
                curr_grid[x][y] = '#'
            elif grid[x][y] == '#':
                curr_grid[x][y] = '.'

    grid = curr_grid
    print_grid()
    print()

    nbr_trees = 0
    nbr_lumb = 0
    for y in range(len(grid[0])):
        for x in range(len(grid)):
            if grid[x][y] == '|':
                nbr_trees +=1
            if grid[x][y] == '#':
                nbr_lumb += 1

    if min >  500:
        val = nbr_lumb * nbr_trees
        if val not in vals:
            vals.append(val)

        left = 1000000000 - min
        i = vals.index(val)
        print('ans ' + str(vals[(left + i - 1) % len(vals)]))


nbr_trees = 0
nbr_lumb = 0
for y in range(len(grid[0])):
    for x in range(len(grid)):
        if grid[x][y] == '|':
            nbr_trees +=1
        if grid[x][y] == '#':
            nbr_lumb += 1

print(nbr_trees * nbr_lumb)
