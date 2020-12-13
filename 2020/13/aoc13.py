#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

earliest = int(lines[0])
buses = lines[1].split(',')

for t in range(earliest, earliest + 100):
    for bus in buses:
        if bus == 'x':
            continue
        if t >= earliest:
            if t % int(bus) == 0:
                print('Part 1: {}'.format(int(bus) * (t - earliest)))
                break
    else:
        continue
    break

t = 0
next_step = int(buses[0])
for i in range(1, len(buses)):
    if buses[i] == 'x':
        continue
        
    bus = int(buses[i])
    while True:
        if (t + i) % bus == 0:
            next_step *= bus
            break

        t += next_step

print('Part 2: {}'.format(t))
