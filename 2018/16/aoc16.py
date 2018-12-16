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


def compare_bf_af(instruction, sample):
    for reg in range(len(regs)):
        regs[reg] = sample[0][reg]

    instruction(sample[1][1], sample[1][2], sample[1][3])

    matches = True
    for reg in range(len(regs)):
        if regs[reg] != sample[2][reg]:
            matches = False

    return matches


regs = [0, 0, 0, 0]
input = []

cnt = 0
with open('input.txt') as fp:
    for line in fp:
        input.append(line.strip())

samples = []
opcode_samples = {}
program = []
part1 = True
i = 0
while i != len(input):
    if part1:
        sample = [input[i][9:-1].split(', '), input[i + 1].split(' '), input[i + 2][9:-1].split(', ')]

        if sample[0][0] == '':
            part1 = False
            continue

        for j in range(len(sample)):
            for k in range(len(sample[j])):
                try:
                    sample[j][k] = int(sample[j][k])
                except:
                    pass

        opcode_samples.setdefault(sample[1][0], [])
        opcode_samples[sample[1][0]].append(sample)

        i += 4
        samples.append(sample)
    else:
        if input[i] != '':
            program.append([int(x) for x in input[i].split(' ')])

        i += 1

instructions = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

cnt = 0
for sample in samples:
    behaves_like = 0
    for instruction in instructions:
        if compare_bf_af(instruction, sample):
            behaves_like += 1

    if behaves_like >= 3:
        cnt += 1


print(cnt)

correct_instructions = [None for x in range(len(instructions))]
while None in correct_instructions:
    nbr_matches = 0
    for instruction in instructions:
        opcode_matches = 0
        matching_opcode = -1
        for opcode, samples in opcode_samples.items():
            all_samples_match = True
            for sample in samples:
                if not compare_bf_af(instruction, sample):
                    all_samples_match = False
                    break

            if all_samples_match:
                opcode_matches += 1
                matching_opcode = opcode

        if opcode_matches == 1:
            correct_instructions[matching_opcode] = instruction
            del opcode_samples[matching_opcode]

regs = [0, 0, 0, 0]
for line in program:
    correct_instructions[line[0]](line[1], line[2], line[3])

print(regs)
