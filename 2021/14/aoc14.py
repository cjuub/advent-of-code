import math
from pathlib import Path

lines = [x.strip() for x in Path('input.txt').open().readlines()]

t = lines[0]
m = {}
for line in lines[2:]:
    k, v = line.split(' -> ')
    m[k] = v

for i in range(10):
    new_t = ''
    for j in range(len(t) - 1):
        pair = t[j] + t[j + 1]
        new_t += t[j] + m[pair]
    new_t += t[-1]
    t = new_t

cnts = {}
for c in t:
    if c not in cnts.keys():
        cnts[c] = 0
    cnts[c] += 1

max_t = (-1, '')
min_t = (99999999999, '')
for c, v in cnts.items():
    max_t = max(max_t, (v, c))
    min_t = min(min_t, (v, c))

print(f"Part 1: {max_t[0] - min_t[0]}")


t = lines[0]
pairs = {}
for j in range(len(t) - 1):
    pair = t[j] + t[j + 1]
    if pair not in pairs.keys():
        pairs[pair] = 0
    pairs[pair] += 1

for i in range(40):
    new_pairs = {}
    for pair, cnt in pairs.items():
        r = pair[0] + m[pair] + pair[1]
        new_p1 = r[0] + r[1]
        new_p2 = r[1] + r[2]
        if new_p1 not in new_pairs.keys():
            new_pairs[new_p1] = cnt
        else:
            new_pairs[new_p1] += cnt
        if new_p2 not in new_pairs.keys():
            new_pairs[new_p2] = cnt
        else:
            new_pairs[new_p2] += cnt

    pairs = new_pairs

cnts = {}
t = lines[0]
for p, v in pairs.items():
    for c in p:
        if c not in cnts.keys():
            cnts[c] = 0
        cnts[c] += v

max_t = (-1, '')
min_t = (999999999999999999999999999999999999, '')
for c, v in cnts.items():
    max_t = max(max_t, (v, c))
    min_t = min(min_t, (v, c))

print(f"Part 2: {math.ceil((max_t[0] - min_t[0]) / 2)}")
