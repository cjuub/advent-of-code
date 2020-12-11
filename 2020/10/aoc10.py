#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

highest = 0
adapters = []
for line in lines:
    line = line.strip()
    adapters.append(int(line))
    highest = max(highest, int(line) + 3)


adapters.append(0)
adapters.append(highest)
adapters = sorted(adapters)

ones = 0
threes = 0
for i in range(len(adapters) - 1):
    diff = adapters[i+1] - adapters[i]
    if diff == 1:
        ones += 1
    elif diff == 3:
        threes += 1
        
print('Part 1: {}'.format(ones * threes))

olds = {}
def good(adapts):
    if len(adapts) < 2:
        return 1
    elif (adapts[1] - adapts[0]) > 3:
        return 0
    
    key = tuple(adapts[1:]), tuple(adapts[:1] + adapts[2:])
    if key in olds.keys():
        return olds[key]
    
    res = good(tuple(adapts[1:])) + good(tuple(adapts[:1] + adapts[2:]))

    olds[key] = res

    return res

print('Part 2: {}'.format(good(adapters[1:])))