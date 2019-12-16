#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

# lines[0] = '12345678'


base_p = [0, 1, 0, -1]

inp = lines[0].strip() * 10

seen = {}

for phase in range(1000):
    print(inp)
    new_list = []

    if inp in seen.keys():
        inp = seen[inp]

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

    # print(new_list)
    seen[inp] = ''.join(new_list)
    inp = ''.join(new_list)

print(''.join(new_list))

