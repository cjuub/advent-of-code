from pathlib import Path

line = [x.strip() for x in Path('input.txt').open().readlines()][0]

spl = line.split(': ')[1]
spl = spl.split(', ')
spl_x = spl[0][2:].split('..')
spl_y = spl[1][2:].split('..')
target_x = (int(spl_x[0]), int(spl_x[1]))
target_y = (int(spl_y[0]), int(spl_y[1]))


hits = []
for init_xv in range(0, 50):
    for init_yv in range(0, 100):
        xv = init_xv
        yv = init_yv
        x = 0
        y = 0
        t = 0
        max_y = 0
        while y > target_y[1]:
            x += xv
            y += yv
            max_y = max(y, max_y)
            if xv != 0:
                xv = xv - 1 if xv > 0 else xv + 1
            yv -= 1

            if y in range(target_y[0], target_y[1]) and x in range(target_x[0], target_x[1]):
                hits.append((init_xv, init_yv, max_y))
                break

            t += 1

print(f'Part 1: {max([x[2] for x in hits])}')


hits = []
for init_xv in range(0, target_x[1] + 1):
    for init_yv in range(target_y[0] - 1, 500):
        xv = init_xv
        yv = init_yv
        x = 0
        y = 0
        t = 0
        while yv > 0 or y > target_y[0]:
            x += xv
            y += yv
            if xv != 0:
                xv = xv - 1 if xv > 0 else xv + 1
            yv -= 1

            if y in range(target_y[0], target_y[1] + 1) and x in range(target_x[0], target_x[1] + 1):
                hits.append((init_xv, init_yv))
                break

            t += 1

print(f'Part 2: {len(hits)}')
