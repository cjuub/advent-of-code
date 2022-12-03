from pathlib import Path

all_instructions = [x.strip() for x in Path("input.txt").open("r").readlines()]
instructions = []
segment_len = 18
divisors = []
offsets = []
modifiers = []
for i in range(0, len(all_instructions), segment_len):
    instructions.append([])
    k = len(instructions) - 1
    for j in range(segment_len):
        instructions[k].append(all_instructions[i+j])
    divisors.append(int(instructions[k][4].split(" ")[-1]))
    offsets.append(int(instructions[k][5].split(" ")[-1]))
    modifiers.append(int(instructions[k][15].split(" ")[-1]))


def calc(op):
    z_values_new = {}
    z_values = {0: 0}
    for i in range(len(instructions)):
        for x, y in z_values.items():
            for digit in range(9, 0, -1):
                candidate = y * 10 + digit
                divisor = divisors[i]
                offset = offsets[i]
                modifier = modifiers[i]

                z = int(x / divisor)
                if x % 26 + offset != digit:
                    z = z * 26 + digit + modifier

                if z in z_values_new:
                    z_values_new[z] = op(z_values_new[z], candidate)
                else:
                    z_values_new[z] = candidate
        z_values = z_values_new.copy()
        z_values_new = {}
    return z_values[0]


print(f"Part 1: {calc(max)}")
print(f"Part 2: {calc(min)}")
