#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

values = [int(x) for x in lines]

cnt = 0
prev = values[0]
for val in values[1:]:
    if val > prev:
        cnt += 1
    prev = val

print(f'Part 1: {cnt}')

cnt = 0
prev = (values[0], values[1], values[2])
for i in range(1, len(values) - 2):
    window = (values[i], values[i+1], values[i+2])
    if sum(window) > sum(prev):
        cnt += 1
    prev = window

print(f'Part 2: {cnt}')
