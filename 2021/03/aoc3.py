from pathlib import Path


with Path("input.txt").open() as fp:
    lines = fp.readlines()


gamma = ''
msbs = []
for i, line in enumerate(lines):
    line = line.strip()
    msbs.append([])
    for j in range(0, len(line)):
        msbs[i].append(line[j])


gamma = ''
epsilon = ''
for i in range(len(msbs[0])):
    high_cnt = 0
    low_cnt = 0
    for j in range(len(msbs)):
        if msbs[j][i] == '1':
            high_cnt += 1
        else:
            low_cnt += 1

    if high_cnt > low_cnt:
        gamma += '1'
        epsilon += '0'
    else:
        gamma += '0'
        epsilon += '1'

print(f'Part 1: {int(gamma, 2) * int(epsilon, 2)}')


i = 0
oxy_vals = set([x.strip() for x in lines])
while len(oxy_vals) != 1:
    high_cnt = 0
    low_cnt = 0
    for val in oxy_vals:
        if val[i] == '1':
            high_cnt += 1
        else:
            low_cnt += 1
    if high_cnt >= low_cnt:
        vals_to_rm = [x for x in oxy_vals if x[i] == '0']
        for val in vals_to_rm:
            oxy_vals.remove(val)
    else:
        vals_to_rm = [x for x in oxy_vals if x[i] == '1']
        for val in vals_to_rm:
            oxy_vals.remove(val)

    i += 1

i = 0
co_vals = set([x.strip() for x in lines])
while len(co_vals) != 1:
    high_cnt = 0
    low_cnt = 0
    for val in co_vals:
        if val[i] == '1':
            high_cnt += 1
        else:
            low_cnt += 1
    if high_cnt >= low_cnt:
        vals_to_rm = [x for x in co_vals if x[i] == '1']
        for val in vals_to_rm:
            co_vals.remove(val)
    else:
        vals_to_rm = [x for x in co_vals if x[i] == '0']
        for val in vals_to_rm:
            co_vals.remove(val)

    i += 1

print(f'Part 2: {int(oxy_vals.pop(), 2) * int(co_vals.pop(), 2)}')

