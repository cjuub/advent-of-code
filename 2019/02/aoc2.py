#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

code = lines[0].split(',')

code_org = code[:]

for x in range(100):
    for y in range(100):
        code = code_org[:]
        pc = 0
        code[1] = x
        code[2] = y
        while True:
            op = int(code[pc])

            # nice int casts bro, real time saver
            if op == 1:
                code[int(code[pc+3])] = int(code[int(code[pc+1])]) + int(code[int(code[pc+2])])
            if op == 2:
                code[int(code[pc+3])] = int(code[int(code[pc+1])]) * int(code[int(code[pc+2])])
            if op == 99:
                break
            pc += 4

        if code[0] == 19690720:
            print(100 * x + y)
            exit(0)

print('done')
