#!/usr/bin/env python3
from ordered_set import OrderedSet

with open('input.txt') as fp:
    lines = fp.readlines()

vals = []
for line in lines:
    line = line.strip()
    vals.append(int(line))

i = 1
prevs = []
preamble = 25
while i < len(vals):
    if i >= preamble:
        a = prevs[-preamble:]
        sums = OrderedSet()
        for j in range(len(a)):
            for k in range(len(a)):
                if j == k:
                    continue
                sums.add(a[j] + a[k])
                
        if vals[i] not in sums:
            print('Part 1: {}'.format(vals[i]))

    prevs.append(vals[i])
    i += 1
    

i = 0
for i in range(len(vals)):
    for j in range(len(vals)):
        r = vals[i:-j]
        if len(r) < 2:
            continue

        smallest = 999999999999999
        largest = -999999999999999
        if sum(r) == 1492208709:
            for v in r:
                smallest = min(smallest, v)
                largest = max(largest, v)

            print('Part 2: {}'.format(smallest + largest))
            exit(0)

    i += 1
