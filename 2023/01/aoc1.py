from pathlib import Path

lines = Path("input.txt").read_text().splitlines()

sum = 0
for line in lines:
    first = None
    last = None
    for c in line:
        if c.isnumeric():
            if not first:
                first = c
            last = c

    assert first is not None
    assert last is not None

    cal = first + last
    sum += int(cal)

print(f"Part 1: {sum}")


NUMBERS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

sum = 0
for line in lines:
    first = None
    last = None
    for i, c in enumerate(line):
        if c.isnumeric():
            if not first:
                first = c
            last = c
        else:
            for number in NUMBERS:
                if line[i:].startswith(number):
                    if not first:
                        first = str(NUMBERS.index(number) + 1)
                    last = str(NUMBERS.index(number) + 1)

    assert first is not None
    assert last is not None

    cal = first + last
    sum += int(cal)

print(f"Part 2: {sum}")
