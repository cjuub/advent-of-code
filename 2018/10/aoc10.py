#!/usr/bin/env python3


class Obj:
    def __init__(self, x, y, vel_x, vel_y):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y


objs = []
min_x = 9999999999
min_y = 9999999999
max_x = -9999999999
max_y = -9999999999
with open('input.txt') as fp:
    for line in fp:
        spl = line.split(',')
        x = int(spl[0][10:])
        y = int(spl[1][:-14])
        vel_x = int(spl[1][19:])
        vel_y = int(spl[2][:-2])

        min_x = min(x, min_x)
        min_y = min(y, min_y)
        max_x = max(x, max_x)
        max_y = max(y, max_y)

        objs.append(Obj(x, y, vel_x, vel_y))


def print_sky(min_x, min_y, objs):
    for y in range(min_y, min_y + 10):
        for x in range(min_x, min_x + 500):
            found = False
            for obj in objs:
                if obj.x == x and obj.y == y:
                    found = True

            if found:
                print('#', end='')
            else:
                print('.', end='')

        print()


secs = 0
last_val = 999999999999
for i in range(10880):
    secs += 1

    print(secs)
    if abs((max_x - min_x) * (max_y - min_y)) > last_val:
        # this stopped secs at 10882 when looping indefinitely, message was scrambled but close.
        # changed loop from while True to surrounding values and found solution at 10880. :)
        break

    last_val = abs((max_x - min_x) * (max_y - min_y))

    min_x = 9999999999
    min_y = 9999999999
    max_x = -9999999999
    max_y = -9999999999
    for obj in objs:
        obj.x += obj.vel_x
        obj.y += obj.vel_y

        min_x = min(obj.x, min_x)
        min_y = min(obj.y, min_y)
        max_x = max(obj.x, max_x)
        max_y = max(obj.y, max_y)

print_sky(min_x, min_y, objs)
