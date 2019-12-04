#!/usr/bin/env python3

passes = []

for i in range(231832, 767346 + 1):
    old_j = -1
    has_two = False
    is_increase = True
    is_good = False

    digits = {}
    digits.setdefault(0)
    for j in str(i):
        if int(j) < int(old_j):
            is_increase = False
        if j == old_j:
            has_two = True

        old_j = j

    s = str(i)
    if is_increase and has_two:
        digits = {}
        for j in s:
            digits.setdefault(j, 0)
            digits[j] = digits[j] + 1

        for j in digits.values():
            if j == 2:
                is_good = True

    # Remove is_good for part 1
    if is_increase and has_two and is_good:
        passes.append(i)

print(len(passes))
