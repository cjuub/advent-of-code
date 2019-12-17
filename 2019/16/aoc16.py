#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

base_p = [0, 1, 0, -1]
inp = lines[0].strip()

for phase in range(100):
    new_list = []

    for k in range(len(inp)):
        p = []
        for i in range(len(inp)):
            for j in range(len(new_list) + 1):
                p.append(base_p[i % len(base_p)])

            if len(p) > len(inp):
                break

        j = 0
        new_d = 0
        for d in inp:
            new_d += int(d) * int(p[(j + 1) % len(p)])
            j += 1
        new_list.append(str(new_d)[-1])

    inp = ''.join(new_list)

print('Part 1: ' + inp[:8])

inp = lines[0].strip() * 10000
inp = inp[5976521:]
inp = [int(i) for i in inp]

for phase in range(100):
    inp_new = []
    sum_prev = 0
    for i in range(len(inp)):
        sum_prev += inp[-i - 1]
        sum_prev %= 10
        inp_new.append(sum_prev)
    inp = list(reversed(inp_new))

print('Part 2: ' + ''.join([str(x) for x in inp[:8]]))
