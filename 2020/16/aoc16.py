#!/usr/bin/env python3
import itertools

with open('input.txt') as fp:
    lines = fp.readlines()
    
data = {}
t = []
tickets = []
parse_mode = 0
for line in lines:
    line = line.strip()
    
    if line == '':
        continue
    
    if parse_mode == 0:
        if line.startswith('your ticket:'):
            parse_mode = 1
            continue

        type = line.split(': ')[0]
        ranges = line.split(': ')[1].split(' or ')
        data[type] = []
        for r in ranges:
            data[type].append(range(int(r.split('-')[0]), int(r.split('-')[1]) + 1))
    if parse_mode == 1:
        if line.startswith('nearby tickets:'):
            parse_mode = 2
            continue
        t = [int(x) for x in line.split(',')]
        continue
    if parse_mode == 2:
        tickets.append([int(x) for x in line.split(',')])


err = 0
good_tickets = []
for nt in tickets:
    has_err = False
    for v in nt:
        in_any = False
        for d, ranges in data.items():
            for r in ranges:
                if v in r:
                    in_any = True

        if not in_any:
            err += v
            has_err = True
            break
            
    if not has_err:
        good_tickets.append(nt)

print('Part 1: {}'.format(err))

oks = {}
for p in itertools.product(data.keys(), range(len(good_tickets[0]))):
    f = p[0]
    i = p[1]
    all_ok = True
    for tick in good_tickets:
        in_any = False
        for r in data[f]:
            if tick[i] in r:
                in_any = True

        if not in_any:
            all_ok = False
            break

    if all_ok:
        if f not in oks.keys():
            oks[f] = []
        oks[f].append(i)
        
poses_done = []
poses = {}
while len(poses_done) != len(good_tickets[0]):
    for i in range(len(good_tickets[0])):
        if i in poses_done:
            continue
        cnt = 0
        the_f = None
        for f, ok in oks.items():
            if f in poses.keys():
                continue
            if i in ok:
                cnt += 1
                the_f = f

        if cnt == 1:
            poses_done.append(i)
            poses[the_f] = i

cnt = 1
for f, i in poses.items():
    if f.startswith('departure'):
        cnt *= t[i]
        

print('Part 2: {}'.format(cnt))
