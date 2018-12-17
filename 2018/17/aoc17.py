#!/usr/bin/env python3

import sys
sys.setrecursionlimit(100000)

def print_grid():
    for y in range(min_y, max_y + 1):
        for x in range(min_x - 2, max_x + 1):
            print(draw_grid[x][y], end='')
        print()


def fill(x, y, dir):
    draw_grid[x][y] = '|'
    moving.append((x, y))

    down = (x, y + 1)
    left = (x - 1, y)
    right = (x + 1, y)

    if grid[down[0]][down[1]] != '#' and down not in moving and 1 <= down[1] <= max_y:
        fill(down[0], down[1], 'down')

    if down not in stopped and grid[down[0]][down[1]] != '#':
        return False

    left_done = False
    if grid[left[0]][left[1]] != '#':
        if left not in moving:
            left_done = fill(left[0], left[1], 'left')
    else:
        left_done = True

    right_done = False
    if grid[right[0]][right[1]] != '#':
        if right not in moving:
            right_done = fill(right[0], right[1], 'right')
    else:
        right_done = True

    leftmost_is_clay = False
    rightmost_is_clay = False
    # back after filling everything to below, left and right when we came from above -> mark water as stopped
    if dir == 'down' and left_done and right_done:
        while left in moving:
            stopped.append(left)
            draw_grid[left[0]][left[1]] = '~'
            left = (left[0] - 1, left[1])

        leftmost_is_clay = grid[left[0]][left[1]] == '#'

        while right in moving:
            stopped.append(right)
            draw_grid[right[0]][right[1]] = '~'
            right = (right[0] + 1, right[1])

        rightmost_is_clay = grid[right[0]][right[1]] == '#'

        stopped.append((x, y))
        draw_grid[x][y] = '~'

    if dir == 'left':
        return left_done or leftmost_is_clay
    elif dir == 'right':
        return right_done or rightmost_is_clay

    return None


min_x = 500
max_x = 500
min_y = 99999
max_y = -1

grid = [['.' for y in range(3000)] for x in range(3000)]

draw_grid = [['.' for y in range(3000)] for x in range(3000)]
draw_grid[500][0] = '+'

moving = []
stopped = []

with open('input.txt') as fp:
    for line in fp:
        first = line.strip().split(', ')[0]
        second = line.strip().split(', ')[1]

        if 'x' in first:
            x = int(first.split('=')[1])
            min_x = min(min_x, x)
            max_x = max(max_x, x)
        else:
            y = int(first.split('=')[1])
            min_y = min(min_y, y)
            max_y = max(max_y, y)

        if 'x' in second:
            ran = (int(second.split('=')[1].split('..')[0]), int(second.split('=')[1].split('..')[1]))
            for x in range(ran[0], ran[1] + 1):
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                grid[x][y] = '#'
                draw_grid[x][y] = '#'

        else:
            ran = (int(second.split('=')[1].split('..')[0]), int(second.split('=')[1].split('..')[1]))
            for y in range(ran[0], ran[1] + 1):
                min_y = min(min_y, y)
                max_y = max(max_y, y)
                grid[x][y] = '#'
                draw_grid[x][y] = '#'


fill(500, min_y, 'down')

print_grid()
print(len(moving))
print(len(stopped))
