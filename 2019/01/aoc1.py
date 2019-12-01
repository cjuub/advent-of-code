#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

sum_p1 = 0
sum_p2 = 0
for line in lines:
    mass = int(line)
    fuel = int(mass / 3) - 2
    sum_p1 += fuel
    sum_p2 += fuel

    while True:
        mass = fuel
        fuel = int(mass / 3) - 2
        if fuel <= 0:
            break
        sum_p2 += fuel

print(sum_p1)
print(sum_p2)
