#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()


def calc(line, i, prev_val, val, prev_sum, outer_sum):
    if i == len(line):
        return val

    if line[i] == ' ':
        i += 1
        
    if line[i] == ')':
        if outer_sum:
            return val, i
        else:
            return val, i
    if line[i] == '(':
        if val == -1:
            val = 1
        
        res = calc(line, i+1, prev_val, -1, False, False)
        if prev_sum:
            val += res[0]
        else:
            val *= res[0]
        
        return calc(line, res[1] + 1, prev_val, val, False, False)

    if line[i] == '+':
        return calc(line, i + 1, prev_val, val, True, outer_sum)
    if line[i] == '*':
        return calc(line, i + 1, prev_val, val, False, outer_sum)
    if line[i].isnumeric():
        if val == -1:
            val = int(line[i])
        elif prev_sum:
            val += int(line[i])
        else:
            val *= int(line[i])
        return calc(line, i + 1, prev_val, val, False, outer_sum)

tot = 0
for line in lines:
    line = line.strip()
    res = calc(line, 0, 0, -1, False, False)

    tot += res

print('Part 1: {}'.format(tot))


def calc2(line, i, vals, prev_sum):
    if i == len(line):
        return vals

    if line[i] == ' ':
        i += 1

    if line[i] == ')':
        prod = 1
        for v in vals:
            prod *= v

        return prod, i
    if line[i] == '(':
        if not vals:
            vals = [1]

        res = calc2(line, i + 1, [], False)
        if prev_sum:
            vals[-1] += res[0]
        else:
            vals.append(res[0])

        return calc2(line, res[1] + 1, vals, False)

    if line[i] == '+':
        return calc2(line, i + 1, vals, True)
    if line[i] == '*':
        return calc2(line, i + 1, vals, False)
    if line[i].isnumeric():
        if not vals:
            vals.append(int(line[i]))
        elif prev_sum:
            vals[-1] += int(line[i])
        else:
            vals.append(int(line[i]))
        return calc2(line, i + 1, vals, False)


tot = 0
for line in lines:
    line = line.strip()
    res = calc2(line, 0, [], False)

    prod = 1
    for v in res:
        prod *= v
        
    tot += prod

print('Part 2: {}'.format(tot))
