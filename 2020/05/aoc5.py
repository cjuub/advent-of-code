#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

highest = 0
ids = []
for line in lines:
    line = line.strip()
    s = (0, 127)
    s2 = (0, 7)
    i = 0
    for l in line:
        if i < 7:
            if l == 'F':
                s = (s[0], int(s[1] - (abs(s[1] - s[0]) / 2)))
            else:
                s = (s[0] + int((abs(s[1] - s[0]) / 2) + 1), s[1])
        else:
            if l == 'L':
                s2 = (s2[0], int(s2[1] - (abs(s2[1] - s2[0]) / 2)))
            else:
                s2 = (s2[0] + int((abs(s2[1] - s2[0]) / 2) + 1), s2[1])
        i += 1

    res = (s[0], s2[0])
    id = res[0] * 8 + res[1]
    highest = max(id, highest)
    ids.append(id)

print('Part 1: {}'.format(highest))

ids = sorted(ids)
i = 91
for id in ids[1:]:
    if id != i:
        print('Part 2: {}'.format(i))
        exit(0)
    i += 1