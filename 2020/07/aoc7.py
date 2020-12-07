#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

bags = {}
for line in lines:
    line = line.strip()
    d = line.split(' bags contain ')
    bags[d[0]] = []
    for d2 in d[1].split(', '):
        nbr = d2.split(' ')[0]
        bags[d[0]].append((nbr, ' '.join(d2.split(' ')[1:-1])))
    

def good(bag, search):
    if len(search) == 1:
        if search[0][0] == 'no':
            return False

    for nbr, s in search:
        if 'shiny gold' in s:
            return True

        if s not in bags.keys():
            continue

        if good(s, bags[s]):
            return True
    
    return False
    

cnt = 0
for bag, search in bags.items():
    if good(bag, search):
        cnt += 1

print('Part 1: {}'.format(cnt))


def good2(search, val):
    if len(search) == 1:
        if search[0][0] == 'no':
            return val

    c = 0
    for nbr, s in search:
        if s not in bags.keys():
            continue

        c += int(nbr) * (good2(bags[s], val) + 1)

    return c


res = good2(bags['shiny gold'], 0)
print('Part 2: {}'.format(res))
