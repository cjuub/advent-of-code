#!/usr/bin/env python3

import z3


def distance(x1, y1, z1, x2, y2, z2):
    dist = 0
    dist += abs(x1 - x2)
    dist += abs(y1 - y2)
    dist += abs(z1 - z2)
    return dist


coords = []
largest = -1
largest_i = -1

with open('input.txt') as fp:
    for line in fp:
        tmp = line.split(',')
        r = int(tmp[3].split('=')[1].strip())
        coords.append((int(tmp[0][5:]), int(tmp[1]), int(tmp[2][:-1]), r))

        if r > largest:
            largest = r
            largest_i = len(coords) - 1

in_range = 0
for coord in coords:
    dist = distance(coords[largest_i][0],coords[largest_i][1],coords[largest_i][2], coord[0], coord[1], coord[2])
    if dist <= coords[largest_i][3]:
        in_range += 1

print('part 1: ' + str(in_range))


# didn't know how to solve this issue, looked up z3 as others had used it and learnt how to use it
o = z3.Optimize()

# set up constraints to find the largest sum of bots
z3_all_in_range = [z3.Int('range' + str(i)) for i in range(len(coords))]
z3_in_range_cnt = z3.Int('cnt')
o.add(z3_in_range_cnt == sum(z3_all_in_range))
bot_cnt = o.maximize(z3_in_range_cnt)

z3_pos = (z3.Int('x'), z3.Int('y'), z3.Int('z'))
for i in range(len(coords)):
    x, y, z, r = coords[i]

    z3_dist = 0
    for coord in [(z3_pos[0], x), (z3_pos[1], y), (z3_pos[2], z)]:
        diff = coord[0] - coord[1]
        z3_dist += z3.If(diff >= 0, diff, -diff)

    z3_in_range = z3.If(z3_dist <= r, 1, 0)
    o.add(z3_all_in_range[i] == z3_in_range)

# optimize on distance to our point
z3_dist = z3.Int('dist')
z3_dist_to_point = z3.If(z3_pos[0] >= 0, z3_pos[0], -z3_pos[0]) + \
                   z3.If(z3_pos[1] >= 0, z3_pos[1], -z3_pos[1]) + \
                   z3.If(z3_pos[2] >= 0, z3_pos[2], -z3_pos[2])

o.add(z3_dist_to_point == z3_dist)

res = o.minimize(z3_dist)

print(o.check())
print('nbr bots: ' + str(bot_cnt.lower()))
print('part 2: ' + str(res.lower()))
