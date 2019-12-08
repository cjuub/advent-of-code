#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

layers = [[]]
layer = 0
cnt = 25 * 6
for i, d in enumerate(lines[0]):
    if i % cnt == 0:
        layer += 1
        layers.append([])
    if d == '\n':
        continue

    layers[layer].append(int(d))

least_zero = 99999999
the_layer = -1

for layer in layers:
    if len(layer) == 0:
        continue

    zeros = layer.count(0)
    if zeros < least_zero:
        the_layer = layer
        least_zero = zeros

print('Part 1: ' + str(the_layer.count(1) * the_layer.count(2)))

print('Part 2:')
cnt = 0
for y in range(6):
    for x in range(25):
        is_filled = False
        for layer in layers:
            if len(layer) == 0:
                continue

            i = layer[cnt]
            if i == 1:
                is_filled = True
                break
            elif i == 0:
                is_filled = False
                break

        if is_filled:
            print('X', end='')
        else:
            print(' ', end='')

        cnt += 1
    print()

