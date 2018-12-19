#!/usr/bin/env python3

def addr(op1, op2, dst):
    regs[dst] = regs[op1] + regs[op2]


def addi(op1, op2, dst):
    regs[dst] = regs[op1] + op2


def mulr(op1, op2, dst):
    regs[dst] = regs[op1] * regs[op2]


def muli(op1, op2, dst):
    regs[dst] = regs[op1] * op2


def banr(op1, op2, dst):
    regs[dst] = regs[op1] & regs[op2]


def bani(op1, op2, dst):
    regs[dst] = regs[op1] & op2


def borr(op1, op2, dst):
    regs[dst] = regs[op1] | regs[op2]


def bori(op1, op2, dst):
    regs[dst] = regs[op1] | op2


def setr(op1, op2, dst):
    regs[dst] = regs[op1]


def seti(op1, op2, dst):
    regs[dst] = op1


def gtir(op1, op2, dst):
    regs[dst] = int(op1 > regs[op2])


def gtri(op1, op2, dst):
    regs[dst] = int(regs[op1] > op2)


def gtrr(op1, op2, dst):
    regs[dst] = int(regs[op1] > regs[op2])


def eqir(op1, op2, dst):
    regs[dst] = int(op1 == regs[op2])


def eqri(op1, op2, dst):
    regs[dst] = int(regs[op1] == op2)


def eqrr(op1, op2, dst):
    regs[dst] = int(regs[op1] == regs[op2])


instructions = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

prog = []
ip = -1
with open('input.txt') as fp:
    for line in fp:
        if line.startswith('#'):
            ip = int(line.split(' ')[1])
            continue

        inp_list = list(line.strip().split(' '))
        instr_index = [x.__name__ for x in instructions].index(inp_list[0])
        prog.append([instructions[instr_index], int(inp_list[1]), int(inp_list[2]), int(inp_list[3])])

regs = [0, 0, 0, 0, 0, 0] # part 1
# regs = [1, 0, 0, 0, 0, 0] # part 2

while True:
    # decompiled of the heavy calc loop:
    # while r5 <= r2
    #     if r3 * r5 == r2
    #         r0 += r3
    #     else
    #         r5++
    #
    # this can be simplified by using modulo instead.
    # modify the code to skip the above decompiled calc and do the one below instead.
    if regs[ip] == 3:
        if regs[2] % regs[3] == 0:
            regs[0] += regs[3]
        regs[ip] = 12

    try:
        instr = prog[regs[ip]]
        instr[0](instr[1], instr[2], instr[3])
    except IndexError:
        break
    regs[ip] += 1

regs[ip] -= 1
print(regs)
