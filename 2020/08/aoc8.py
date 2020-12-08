#!/usr/bin/env python3
from ordered_set import OrderedSet

with open('input.txt') as fp:
    lines = fp.readlines()
    
ram = []

for line in lines:
    line = line.strip()

    instr = line.split(' ')[0]
    v = int(line.split(' ')[1])
    ram.append((instr, v))


a = 0
pc = 0
olds = OrderedSet()

old_cnt = 0
while True:
    instr, v = ram[pc]

    if pc in olds:
        old_cnt += 1
        
    if old_cnt > 0:
        break
        
    olds.add(pc)
    
    if instr == 'acc':
        a += v
    elif instr == 'jmp':
        pc += v
        continue
    elif instr == 'nop':
        pass
        
    pc += 1

print('Part 1: {}'.format(a))

for b in olds:
    old_val = ram[b]
    if ram[b][0] == 'acc':
        continue
    elif ram[b][0] == 'jmp':
        ram[b] = ('nop', 0)
    else:
        ram[b] = ('jmp', ram[b][1])

    olds2 = OrderedSet()

    a = 0
    pc = 0
    old_cnt = 0
    while True:
        if (pc >= len(ram)):
            print('Part 2: {}'.format(a))
            exit(0)

        instr, v = ram[pc]

        if pc in olds2:
            old_cnt += 1

        if old_cnt > 500:
            ram[b] = old_val
            break

        olds2.add(pc)

        if instr == 'acc':
            a += v
        elif instr == 'jmp':
            pc += v
            continue
        elif instr == 'nop':
            pass

        pc += 1
