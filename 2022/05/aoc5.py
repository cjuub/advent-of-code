from pathlib import Path

lines = Path("input.txt").open().readlines()

index_line = lines[8]
reversed_stacks = [[] for x in range(len(index_line.split("  ")))]
for line in lines:
    if line == index_line:
        break
    for i, l in enumerate(line):
        if index_line[i] != " " and index_line[i] != "\n" and l != " ":
            reversed_stacks[int(index_line[i])-1].append(l)


stacks = []
for i, reversed_stack in enumerate(reversed_stacks):
    stacks.append(list(reversed(reversed_stack)))


good_steps = []
for step in lines[10:]:
    step = step.replace("move ", "")
    step = step.replace(" from ", " ")
    step = step.replace(" to ", " ")
    step = step.strip()

    cnt = int(step.split(" ")[0])
    src = int(step.split(" ")[1]) - 1
    dst = int(step.split(" ")[2]) - 1
    good_steps.append((cnt, src, dst))


for cnt, src, dst in good_steps:
    for i in range(cnt):
        stacks[dst].append(stacks[src].pop())

res = ""
for stack in stacks:
    res += stack.pop()

print(f"Part 1: {res}")

stacks = []
for i, reversed_stack in enumerate(reversed_stacks):
    stacks.append(list(reversed(reversed_stack)))

for cnt, src, dst in good_steps:
    to_move = []
    for i in range(cnt):
        to_move.append(stacks[src].pop())
    for i in range(cnt):
        stacks[dst].append(to_move.pop())

res = ""
for stack in stacks:
    res += stack.pop()

print(f"Part 2: {res}")
