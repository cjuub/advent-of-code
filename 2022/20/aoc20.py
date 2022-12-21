from pathlib import Path

file = [int(x) for x in Path("input.txt").open("r").readlines()]
unique_file = [(i, x) for i, x in enumerate(file)]
unique_file_orig = unique_file[:]

for x in unique_file_orig:
    src_index = unique_file.index(x)
    src_val = x[1]
    dst_index = (src_index + src_val) % (len(unique_file) - 1)
    dst_val = unique_file.pop(src_index)
    unique_file.insert(dst_index, dst_val)

zero_index = -1
for i, (index, val) in enumerate(unique_file):
    if val == 0:
        zero_index = i
        break

l = [x[1] for x in unique_file]
res = l[(zero_index + 1000) % len(l)] + l[(zero_index + 2000) % len(l)] + l[(zero_index + 3000) % len(l)]
print(f"Part 1: {res}")

dec_key = 811589153
unique_file = [(i, x * dec_key) for i, x in enumerate(file)]
unique_file_orig = unique_file[:]

for i in range(10):
    for x in unique_file_orig:
        src_index = unique_file.index(x)
        src_val = x[1]
        dst_index = (src_index + src_val) % (len(unique_file) - 1)
        dst_val = unique_file.pop(src_index)
        unique_file.insert(dst_index, dst_val)

zero_index = -1
for i, (index, val) in enumerate(unique_file):
    if val == 0:
        zero_index = i
        break

l = [x[1] for x in unique_file]
res = l[(zero_index + 1000) % len(l)] + l[(zero_index + 2000) % len(l)] + l[(zero_index + 3000) % len(l)]
print(f"Part 2: {res}")
