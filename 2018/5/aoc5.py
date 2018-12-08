#!/usr/bin/env python3


input = ''
with open('input.txt') as fp:
    for line in fp:
        input += line.strip()

input_orig = input

last_input = ""
while input != last_input:
    last_input = input
    for i in range(ord('z') - ord('a') + 1):
        input = input.replace(chr(ord('a') + i) + chr(ord('A') + i), '')
        input = input.replace(chr(ord('A') + i) + chr(ord('a') + i), '')


print(len(input))


shortest = 99999999
for polymer in range(ord('z') - ord('a') + 1):
    input = input_orig
    input = input.replace(chr(ord('a') + polymer), '')
    input = input.replace(chr(ord('A') + polymer), '')

    last_input = ""
    while input != last_input:
        last_input = input
        for i in range(ord('z') - ord('a') + 1):
            input = input.replace(chr(ord('a') + i) + chr(ord('A') + i), '')
            input = input.replace(chr(ord('A') + i) + chr(ord('a') + i), '')

    shortest = min(shortest, len(input))

print(shortest)

