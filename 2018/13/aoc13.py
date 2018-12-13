#!/usr/bin/env python3

lines = []
longest_line = -1
with open('input.txt') as fp:
    for line in fp:
        lines.append(list(line[:-1]))
        longest_line = max(longest_line, len(line))


grid = [['' for y in range(len(lines) + 1)] for x in range(longest_line)]
orig_grid = [['' for y in range(len(lines) + 1)] for x in range(longest_line)]

carts = '<>^v'
turns = '\\/+'

cart_poses = {}
y = 0
cart_id = 0
for line in lines:
    x = 0
    for ch in line:
        if ch in carts:
            cart_poses[(x, y)] = (ch, cart_id)
            cart_id += 1
        grid[x][y] = ch
        orig_grid[x][y] = ch

        if ch in '><':
            orig_grid[x][y] = '-'
        elif ch in '^v':
            orig_grid[x][y] = '|'

        x += 1
    y += 1


def print_tracks(grid):
    for y in range(len(grid[0])):
        for x in range(len(grid)):
            print(grid[x][y], end='')
        print()


inter_changes = ['left', 'straight', 'right']
next_inters = {}
prev_poses = {}


for pos, cart in cart_poses.items():
    x_change = 0
    y_change = 0
    if cart == '^':
        y_change = -1
    elif cart == 'v':
        y_change = 1
    elif cart == '>':
        x_change = 1
    elif cart == '<':
        x_change = -1

    prev_poses[cart[1]] = (x_change, y_change)


def step(grid, cart, x, y):
    x_change = 0
    y_change = 0
    cart_change = cart[0]

    curr = orig_grid[x][y]
    if curr in turns:
        prev_x, prev_y = prev_poses[cart[1]]
        if curr == '\\':
            if prev_x == -1:
                y_change = -1
                cart_change = '^'
            elif prev_x == 1:
                y_change = 1
                cart_change = 'v'
            elif prev_y == 1:
                x_change = 1
                cart_change = '>'
            else:
                x_change = -1
                cart_change = '<'
        elif curr == '/':
            if prev_x == -1:
                y_change = 1
                cart_change = 'v'
            elif prev_x == 1:
                y_change = -1
                cart_change = '^'
            elif prev_y == 1:
                x_change = -1
                cart_change = '<'
            else:
                x_change = 1
                cart_change = '>'
        elif curr == '+':
            next_inters.setdefault(cart[1], 0)
            next_inter = next_inters[cart[1]]

            if next_inter == 0: # left
                if prev_x == -1:
                    y_change = 1
                    cart_change = 'v'
                elif prev_x == 1:
                    y_change = -1
                    cart_change = '^'
                elif prev_y == 1:
                    x_change = 1
                    cart_change = '>'
                else:
                    x_change = -1
                    cart_change = '<'
            elif next_inter == 1: # straight
                if cart[0] == '^':
                    y_change = -1
                elif cart[0] == 'v':
                    y_change = 1
                elif cart[0] == '>':
                    x_change = 1
                elif cart[0] == '<':
                    x_change = -1
            else: # right
                if prev_x == -1:
                    y_change = -1
                    cart_change = '^'
                elif prev_x == 1:
                    y_change = 1
                    cart_change = 'v'
                elif prev_y == 1:
                    x_change = -1
                    cart_change = '<'
                else:
                    x_change = 1
                    cart_change = '>'

            next_inters[cart[1]] = (next_inters[cart[1]] + 1) % 3
    else:
        if cart[0] == '^':
            y_change = -1
        elif cart[0] == 'v':
            y_change = 1
        elif cart[0] == '>':
            x_change = 1
        elif cart[0] == '<':
            x_change = -1


    grid[x][y] = orig_grid[x][y]
    if grid[x + x_change][y + y_change] in carts:
        grid[x][y] = orig_grid[x][y]
        grid[x+x_change][y+y_change] = orig_grid[x+x_change][y+y_change]
        del cart_poses[(x, y)]
        del cart_poses[(x + x_change, y + y_change)]

        # print('Solution 1: ' + str(x + x_change) + ',' + str(y + y_change))
        # exit(0)

    else:
        del cart_poses[(x, y)]
        grid[x + x_change][y + y_change] = cart_change
        cart_poses[(x + x_change, y + y_change)] = (cart_change, cart[1])
        prev_poses[cart[1]] = (x_change, y_change)


for tick in range(1000000000):
    cart_poses_list = sorted(cart_poses.keys(), key=lambda x: (x[1], x[0]))

    for cart_pos in cart_poses_list:
        try:
            cart = cart_poses[cart_pos]
        except:
            # This cart was removed, skip it
            continue

        step(grid, cart, cart_pos[0], cart_pos[1])

    if len(cart_poses.keys()) == 1:
        print('Solution 2: ' + str(cart_poses.keys()))
        exit(0)
