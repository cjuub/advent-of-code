from pathlib import Path

data = Path("input.txt").open("r").readlines()[0].strip()

buffer = []
buffer_len = 4
i = 0
for c in data:
    if len(buffer) == buffer_len:
        buffer = buffer[1:]
    buffer.append(c)
    i += 1
    if len(set(buffer)) == buffer_len:
        break

print(f"Part 1: {i}")

buffer = []
buffer_len = 14
i = 0
for c in data:
    if len(buffer) == buffer_len:
        buffer = buffer[1:]
    buffer.append(c)
    i += 1
    if len(set(buffer)) == buffer_len:
        break

print(f"Part 2: {i}")
