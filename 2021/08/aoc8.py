from pathlib import Path

lines = [x.strip() for x in Path("input.txt").open().readlines()]
digs = []
for line in lines:
    s = line.split(' | ')
    digs.append((s[0].split(' '), s[1].split(' ')))

cnt = 0
lens = [2, 4, 3, 7]
for inps, outs in digs:
    for out in outs:
        if len(out) in lens:
            cnt += 1

print(f"Part 1: {cnt}")

cnt = 0
for inps, outs in digs:
    res = {}
    for inp in inps:
        if len(inp) == 2:
            res[inp] = 1
        elif len(inp) == 4:
            res[inp] = 4
        elif len(inp) == 3:
            res[inp] = 7
        elif len(inp) == 7:
            res[inp] = 8

    for key in res.keys():
        inps.remove(key)

    res_rev = {}
    for key, val in res.items():
        res_rev[val] = key

    for inp in inps:
        if len(inp) == 6:
            if set(list(res_rev[4])).issubset(set(list(inp))):
                res[inp] = 9
                res_rev[9] = inp
                inps.remove(inp)
                break
    for inp in inps:
        if len(inp) == 6:
            if set(list(res_rev[7])).issubset(set(list(inp))):
                res[inp] = 0
                res_rev[0] = inp
                inps.remove(inp)
                break
    for inp in inps:
        if len(inp) == 6:
            res[inp] = 6
            res_rev[6] = inp
            inps.remove(inp)
            break

    for inp in inps:
        if len(inp) == 5:
            if set(list(res_rev[7])).issubset(set(list(inp))):
                res[inp] = 3
                res_rev[3] = inp
                inps.remove(inp)
                break

    for inp in inps:
        if len(inp) == 5:
            if set(list(res_rev[6])).issuperset(set(list(inp))):
                res[inp] = 5
                res_rev[5] = inp
                inps.remove(inp)
                break
    res[inps[0]] = 2

    out_val = ''
    for out in outs:
        for key, val in res.items():
            if sorted(out) == sorted(key):
                out_val += str(val)
    cnt += int(out_val)

print(f"Part 2: {cnt}")
