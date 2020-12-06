#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

cnt = 0
q = set()
for line in lines:
    line = line.strip()
    if line == '':
        cnt += len(q)
        q = set()
        continue
    
    for l in line:
        q.add(l)

cnt += len(q)
print('Part 1: {}'.format(cnt))

sets = []
cnt = 0
q = set()
for line in lines:
    line = line.strip()
    if line == '':
        unions = sets[0]
        for s in sets:
            unions = s.intersection(unions)
        cnt += len(unions)
        sets = []
        continue

    for l in line:
        q.add(l)

    sets.append(q)
    q = set()

unions = sets[0]
for s in sets:
    unions = s.intersection(unions)
cnt += len(unions)

print('Part 2: {}'.format(cnt))
