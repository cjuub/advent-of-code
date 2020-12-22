#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

parse_mode = 0
rules = {}
msgs = []
for line in lines:
    line = line.strip()

    if line == '':
        parse_mode = 1
        continue

    if parse_mode == 0:
        r = int(line.split(': ')[0])
        d = line.split(': ')[1]
        if not d.startswith('"'):
            ds = d.split(' | ')
            rules[r] = []
            for d1 in ds:
                vals = []
                for v in d1.split(' '):
                    vals.append(int(v))
                rules[r].append(vals)
        else:
            rules[r] = d[1:-1]
    else:
        msgs.append(line)


def calc(rule, curr):
    ret = []
    for alt in rules[rule]:
        res = curr[:]
        for r in alt:
            if isinstance(rules[r], str):
                for idx, val in enumerate(res):
                    res[idx] = val + rules[r]
            else:
                res = calc(r, res)
        ret.extend(res)
    return ret


ret = calc(0, [""])

cnt = 0
for msg in msgs:
    if msg in ret:
        cnt += 1

print(f'Part 1: {cnt}')

# TODO: Part 2 without lark lib
#rules[8] = [[42], [42, 8]]
#rules[11] = [[42, 31], [42, 11, 31]]


def part_2_lark():
    with open("input.txt") as f:
        rules, messages = f.read().split("\n\n")

    from lark import Lark

    rules = rules.replace('8: 42', '8: 42 | 42 8')
    rules = rules.replace('11: 42 31', '11: 42 31 | 42 11 31')
    rules = rules.translate(str.maketrans("0123456789", "abcdefghij"))
    parser = Lark(rules, start="a")

    def try_parse(msg):
        try:
            parser.parse(msg)
            return True
        except:
            return False

    return len([msg for msg in messages.splitlines() if try_parse(msg)])

print(f"Part 2: {part_2_lark()}")
