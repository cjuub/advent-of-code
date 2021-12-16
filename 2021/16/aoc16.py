from pathlib import Path

lines = [x.strip() for x in Path('input.txt').open().readlines()]
line = lines[0]

p = ''
for c in line:
    p += '{:04b}'.format(int(c, 16))


def parse(p, i, data):
    if not p[i:] or int(p[i:], 2) == 0:
        return 0

    k = i

    ver = int(p[i:i+3], 2)
    i += 3
    data[0] += ver
    ident = int(p[i:i+3], 2)
    i += 3
    if ident == 4:
        val = ''
        while int(p[i], 2) == 1:
            val += p[i+1:i+5]
            i += 5
        val += p[i+1:i+5]
        i += 5
    else:
        len_id = int(p[i], 2)
        i += 1
        if len_id == 0:
            length = int(p[i:i+15], 2)
            i += 15
            j = i
            while i - j != length:
                i += parse(p, i, data)
        else:
            length = int(p[i:i+11], 2)
            i += 11
            for _ in range(length):
                i += parse(p, i, data)

    return i - k


data = [0]
parse(p, 0, data)
print(f"Part 1: {data[0]}")
