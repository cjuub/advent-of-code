#!/usr/bin/env python3


def distance(a, b):
    dist = 0
    dist += abs(a[0] - b[0])
    dist += abs(a[1] - b[1])
    dist += abs(a[2] - b[2])
    dist += abs(a[3] - b[3])
    return dist


coords = []
with open('input.txt') as fp:
    for line in fp:
        coords.append(tuple([int(x) for x in line.strip().split(',')]))

found = {coords[0]}
consts = []
while True:
    added = False
    for c1 in list(found):
        for c2 in coords:
            if c1 == c2 or c2 in found:
                continue

            if distance(c1, c2) <= 3:
                found.add(c2)
                added = True

    if not added:
        consts.append(list(found))
        for coord in found:
            try:
                del coords[coords.index(coord)]
            except ValueError:
                pass

        if len(coords) > 0:
            found = {coords[0]}

    if len(coords) == 0:
        break

print(len(consts))
