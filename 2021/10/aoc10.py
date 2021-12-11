from pathlib import Path

lines = [x.strip() for x in Path("input.txt").open().readlines()]

close = {')': '(', ']': '[', '}': '{', '>': '<'}

corrupt = []
for line in lines:
    currs = [line[0]]
    for c in line[1:]:
        if c in close.keys():
            curr = currs.pop()
            if close[c] != curr:
                corrupt.append((line, c))
                break
        else:
            currs.append(c)

score = 0
points = {')': 3, ']': 57, '}': 1197, '>': 25137}
for corr, c in corrupt:
    score += points[c]

print(f"Part 1: {score}")


incs = []
for line in lines:
    if line not in [x[0] for x in corrupt]:
        incs.append(line)

close2 = {'(': ')', '[': ']', '{': '}', '<': '>'}

completions = []
for line in incs:
    currs = [line[0]]
    expected = [close2[line[0]]]
    for c in line[1:]:
        if c in close.keys():
            curr = currs.pop()
            expected.pop()
        else:
            currs.append(c)
            expected.append(close2[c])

    completions.append(''.join(reversed(expected)))

points = {')': 1, ']': 2, '}': 3, '>': 4}
scores = []
for comp in completions:
    score = 0
    for c in comp:
        score *= 5
        score += points[c]
    scores.append(score)

print(f"Part 2: {sorted(scores)[int(len(scores) / 2)]}")


