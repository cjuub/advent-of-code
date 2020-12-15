#!/usr/bin/env python3

inp = '6,19,0,5,7,13,1'.split(',')
# inp = '0,3,6'.split(',')

nums = []
i = 0
prevs = {}
for val in inp:
    nums.append(int(val))
    prevs[int(val)] = []
    prevs[int(val)].append(i)
    i += 1
    
last = nums[i - 1]

while True:
    if len(prevs[last]) == 1:
        last = 0
        prevs[last].append(i)
    else:
        last = prevs[last][-1] - prevs[last][-2]
        
        if last not in prevs.keys():
            prevs[last] = []

        prevs[last].append(i)

    if i == 2020 - 1:
        print('Part 1: {}'.format(last))

    if i == 30000000 - 1:
        print('Part 2: {}'.format(last))
        break

    i += 1
