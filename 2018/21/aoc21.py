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

regs = [9566170, 0, 0, 0, 0, 0] # part 1
# regs = [0, 0, 0, 0, 0, 0] # part 2

vals = set()
i = 0
while True:
    try:
        instr = prog[regs[ip]]
        instr[0](instr[1], instr[2], instr[3])
    except IndexError:
        break
    regs[ip] += 1

    if regs[ip] == 28:
        set_len = len(vals)
        vals.add(regs[4])
        if set_len == len(vals):
            exit(0)
        print(str(i) + ' ' + str(regs))
        i += 1

regs[ip] -= 1
print(regs)
