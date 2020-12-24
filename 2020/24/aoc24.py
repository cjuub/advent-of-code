#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

flips = []
for line in lines:
    line = line.strip()
    
    flip = []
    i = 0
    while i < len(line):
        if line[i] == 's' or line[i] == 'n':
            flip.append(line[i] + line[i+1])
            i += 1
        else:
            flip.append(line[i])
        
        i += 1

    flips.append(flip)
            

flipped = {}
paths = []
for flip in flips:
    path = [(0, 0, 0)]
    
    x = 0
    y = 0
    z = 0
    for step in flip:
        if step == 'e':
            y -= 1
            x += 1
        elif step == 'ne':
            x += 1
            z -= 1
        elif step == 'se':
            y -= 1
            z += 1
        elif step == 'w':
            y += 1
            x -= 1
        elif step == 'nw':
            y += 1
            z -= 1
        else:
            z += 1
            x -= 1

        next_coord = (x, y, z)
        path.append((x, y, z))

    if path[-1] in flipped:
        flipped[path[-1]] = not flipped[path[-1]]
    else:
        flipped[path[-1]] = True


blacks = set()
for tile, is_black in flipped.items():
    if is_black:
        blacks.add(tile)

    
print(f'Part 1: {len(blacks)}')

for day in range(100):
    to_flip = set()
    adj_whites = set()
    for black in blacks:
        cnt = 0
        for coord in [(black[0] + 1, black[1], black[2] - 1),
                       (black[0] + 1, black[1] - 1, black[2]),
                       (black[0], black[1] - 1, black[2] + 1),
                       (black[0], black[1] + 1, black[2] - 1),
                       (black[0] - 1, black[1] + 1, black[2]),
                       (black[0] - 1, black[1], black[2] + 1)]:
            if coord in blacks:
                cnt += 1
            else:
                adj_whites.add(coord)
        
        if cnt == 0 or cnt > 2:
            to_flip.add(black)
    
    for white in adj_whites:
        cnt = 0
        for coord in [(white[0] + 1, white[1], white[2] - 1),
                      (white[0] + 1, white[1] - 1, white[2]),
                      (white[0], white[1] - 1, white[2] + 1),
                      (white[0], white[1] + 1, white[2] - 1),
                      (white[0] - 1, white[1] + 1, white[2]),
                      (white[0] - 1, white[1], white[2] + 1)]:
            if coord in blacks:
                cnt += 1

        if cnt == 2:
            to_flip.add(white)

    for f in to_flip:
        if f in blacks:
            blacks.remove(f)
        else:
            blacks.add(f)

print(f'Part 2: {len(blacks)}')
