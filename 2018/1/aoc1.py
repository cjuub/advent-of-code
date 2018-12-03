#!/usr/bin/env python3


ans = 0

found_freqs = []
with open('input.txt') as fp:
    for line in fp:
        if line[0] == '+':
            ans += int(line[1:])
        else:
            ans -= int(line[1:])

        if ans in found_freqs:
            print(ans)
        found_freqs.append(ans)

print(ans)

ans = 0
found_freqs = []
while True:
    with open('input.txt') as fp:
        for line in fp:
            if line[0] == '+':
                ans += int(line[1:])
            else:
                ans -= int(line[1:])

            if ans in found_freqs:
                print(ans)
                exit(0)

            found_freqs.append(ans)

