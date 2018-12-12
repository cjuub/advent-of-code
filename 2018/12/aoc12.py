#!/usr/bin/env python3

evos = {}
init = None
with open('input.txt') as fp:
    for line in fp:
        if not init:
            init = line.split(': ')[1].strip()
            continue

        if line == '\n':
            continue

        split = line.split(' => ')
        evos[split[0].strip()] = split[1].strip()

gen = '.' * 1000 + init + '.' * 1000
print('0: '+ gen)
first = True

first_index = gen.find('#')
prev_sum = 0

#for j in range(1, 21): # solution 1
for j in range(1, 50000000000): # solution 2 wtf
    next_gen = '.' * (len(init) + 1000 * 2)

    for i in range(2, len(gen) - 2):
        curr = gen[i - 2] + gen[i-1] + gen[i] + gen[i+1] + gen[i+2]

        if curr not in evos.keys():
            next_gen_list = list(next_gen)
            next_gen_list[i] = '.'
            next_gen = ''.join(next_gen_list)
            continue

        next_gen_list = list(next_gen)
        next_gen_list[i] = evos[curr]
        next_gen = ''.join(next_gen_list)

    gen = next_gen

    offs = first_index
    sum = 0
    for s in range(len(next_gen)):
        if next_gen[s] == '#':
            sum += s - offs

    # print(str(j) + ': ' + next_gen + ' ' + str(sum))

    # wow this actually worked, eventually the sum difference becomes stable, so we can manually figure out the answer.
    print(str(sum) + ' + ' + str(sum - prev_sum))
    print(sum + (sum - prev_sum) * (50000000000 - j)) # the answer after a while

    prev_sum = sum
