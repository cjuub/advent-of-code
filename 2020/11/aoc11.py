#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

input = []
for line in lines:
    line = line.strip()
    input.append(line)

def adjacents(x, y):
    return [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]

def directions():
    return [(- 1,- 1), (0,- 1), (1,- 1), (- 1, 0), (1, 0), (- 1, 1), (0, 1), (1, 1)]



def copy_grid(grid):
    copy = [['' for y in range(len(grid[0]))] for x in range(len(grid))]
    for y in range(len(grid[0])):
        for x in range(len(grid)):
            copy[x][y] = grid[x][y]

    return copy


grid = [['' for y in range(len(input))] for x in range(len(input[0]))]
for y in range(len(input)):
    for x in range(len(input[0])):
        grid[x][y] = input[y][x]

def comp_grid(g1, g2):
    for y in range(len(g1[0])):
        for x in range(len(g1)):
            if g1[x][y] != g2[x][y]:
                return False
    
    return True


def occ_in_dir(grid, x, y, direction):
    if x < 0 or y < 0:
        return False
    elif x > len(grid) - 1 or y > len(grid[0]) - 1:
        return False
    elif grid[x][y] == 'L':
        return False
    elif grid[x][y] == '#':
        return True
    else:
        return occ_in_dir(grid, x + direction[0], y + direction[1], direction)


orig_grid = copy_grid(grid)

g2 = copy_grid(orig_grid)
for i in range(100):
    grid = copy_grid(g2)

    for y in range(len(input)):
        for x in range(len(input[0])):

            if grid[x][y] == '.':
                pass
            elif grid[x][y] == 'L':
                any_adj = False
                for j, adj in enumerate(adjacents(x, y)):
                    if adj[0] < 0 or adj[1] < 0:
                        continue
                    elif adj[0] > len(grid) - 1 or adj[1] > len(grid[0]) - 1:
                        continue

                    if grid[adj[0]][adj[1]] == '#':
                        any_adj = True
                        break

                if not any_adj:
                    g2[x][y] = '#'
            else:
                cnt = 0
                for j, adj in enumerate(adjacents(x, y)):
                    if x + adj[0] < 0 or y + adj[1] < 0:
                        continue
                    elif adj[0] > len(grid) - 1 or adj[1] > len(grid[0]) - 1:
                        continue

                    if grid[adj[0]][adj[1]] == '#':
                        cnt += 1

                if cnt >= 4:
                    g2[x][y] = 'L'

    #         print(grid[x][y], end='')
    #     print()
    # print()

    if comp_grid(grid, g2):
        break

nbr = 0
for y in range(len(input)):
    for x in range(len(input[0])):
        if grid[x][y] == '#':
            nbr += 1
    #     print(grid[x][y], end='')
    # print()

print('Part 1: {}'.format(nbr))

grid = copy_grid(orig_grid)
g2 = copy_grid(orig_grid)
for i in range(100):
    grid = copy_grid(g2)

    for y in range(len(input)):
        for x in range(len(input[0])):

            if grid[x][y] == '.':
                pass
            elif grid[x][y] == 'L':
                any_adj = False
                for direction in directions():
                    if occ_in_dir(grid, x + direction[0], y + direction[1], direction):
                        any_adj = True
                        break

                if not any_adj:
                    g2[x][y] = '#'
            else:
                cnt = 0
                for direction in directions():
                    if occ_in_dir(grid, x + direction[0], y + direction[1], direction):
                        cnt += 1

                if cnt >= 5:
                    g2[x][y] = 'L'

    #         print(grid[x][y], end='')
    #     print()
    # print()

    if comp_grid(grid, g2):
        break

nbr = 0
for y in range(len(input)):
    for x in range(len(input[0])):
        if grid[x][y] == '#':
            nbr += 1
    #     print(grid[x][y], end='')
    # print()
    
print('Part 1: {}'.format(nbr))
