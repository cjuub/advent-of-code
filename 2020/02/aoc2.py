#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

nbr = 0
for line in lines:
    a = line.split(' ')

    low = int(a[0].split('-')[0])
    high = int(a[0].split('-')[1])
    l = a[1][:-1]
    w = a[2]

    c = w.count(l)
    if c >= low and c <= high:
        nbr += 1

print('Part 1: {}'.format(nbr))

nbr = 0
for line in lines:
    a = line.split(' ')
    
    low = int(a[0].split('-')[0])
    high = int(a[0].split('-')[1])
    l = a[1][:-1]
    w = a[2]

    ok = False
    if w[low - 1] == l:
        if w[high - 1] == l:
            ok = False
        else:
            ok = True
    elif w[high - 1] == l:
        if w[low - 1] == l:
            ok = False
        else:
            ok = True

    if ok:
        nbr += 1
    
print('Part 2: {}'.format(nbr))
