#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

a = 0
b = 0
c = 0
for line in lines:
    a = int(line)
    for line2 in lines:
        b = int(line2)
        
        if a + b == 2020:
            print('Part 1: {}'.format(a * b))
        for line3 in lines:
            c = int(line3)
            if a + b + c == 2020:
                print('Part 2: {}'.format(a * b * c))
