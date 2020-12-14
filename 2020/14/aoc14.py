#!/usr/bin/env python3
import itertools
import copy

with open('input.txt') as fp:
    lines = fp.readlines()
    
mem = {}
for line in lines:
    line = line.strip()
    addr = line.split(' = ')[0]
    
    if addr.startswith('mask'):
        mask = line.split(' = ')[1]
    else:
        addr = addr[4:-1]

        val = int(line.split(' = ')[1])
        val = list(bin(val)[2:].zfill(36))
    
        for i, b in enumerate(mask):
            if b != 'X':
                val[i] = b
            
        mem[int(''.join(addr))] = ''.join(val)

sum = 0
for m in mem.values():
    sum += int(m, 2)

print('Part 1: {}'.format(sum))

mem = {}
for line in lines:
    line = line.strip()
    addr = line.split(' = ')[0]

    if addr.startswith('mask'):
        mask = line.split(' = ')[1]
    else:
        addr = int(addr[4:-1])
        addr = list(bin(addr)[2:].zfill(36))

        val = int(line.split(' = ')[1])

        n_floating = 0
        for i, b in enumerate(mask):
            if b == '0':
                continue
            if b == 'X':
                n_floating += 1

            addr[i] = b

        addr_orig = copy.deepcopy(addr)
        for bits in itertools.product([0, 1], repeat=n_floating):
            addr = copy.deepcopy(addr_orig)
            x_i = 0
            for i, b in enumerate(addr):
                if b == 'X':
                    addr[i] = str(bits[x_i])
                    x_i += 1
                else:
                    addr[i] = b

            mem[int(''.join(addr), 2)] = val

sum = 0
for m in mem.values():
    sum += m

print('Part 2: {}'.format(sum))
