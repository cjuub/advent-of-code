from pathlib import Path

lines = [x.strip() for x in Path("input.txt").open("r").readlines()]

monkeys = {}
for line in lines:
    s = line.split(": ")

    try:
        monkeys[s[0]] = int(s[1])
    except ValueError:
        monkeys[s[0]] = s[1]


def yell(curr, yell_cache):
    job = monkeys[curr]
    if isinstance(job, int):
        yell_cache[curr] = job
        return job

    s = job.split(" ")
    left = s[0]
    op = s[1]
    right = s[2]
    if left in yell_cache and right in yell_cache:
        return int(eval(f"{yell_cache[left]} {op} {yell_cache[right]}"))
    elif left in yell_cache:
        return int(eval(f"{yell_cache[left]} {op} {yell(right, yell_cache)}"))
    elif right in yell_cache:
        return int(eval(f"{yell(left, yell_cache)} {op} {yell_cache[right]}"))

    return int(eval(f"{yell(left, yell_cache)} {op} {yell(right, yell_cache)}"))


yell_cache = {}
print(f"Part 1: {yell('root', yell_cache)}")


def yell_root_diff(curr, yell_cache):
    job = monkeys[curr]
    if isinstance(job, int):
        yell_cache[curr] = job
        return job

    s = job.split(" ")
    left = s[0]
    op = s[1]
    right = s[2]
    if left in yell_cache and right in yell_cache:
        yell_cache[curr] = int(eval(f"{yell_cache[left]} {op} {yell_cache[right]}"))
        return yell_cache[curr]
    elif left in yell_cache:
        yell_cache[curr] = int(eval(f"{yell_cache[left]} {op} {yell_root_diff(right, yell_cache)}"))
        return yell_cache[curr]
    elif right in yell_cache:
        yell_cache[curr] = int(eval(f"{yell_root_diff(left, yell_cache)} {op} {yell_cache[right]}"))
        return yell_cache[curr]

    if curr == "root":
        return yell_root_diff(left, yell_cache) - yell_root_diff(right, yell_cache)

    yell_cache[curr] = int(eval(f"{yell_root_diff(left, yell_cache)} {op} {yell_root_diff(right, yell_cache)}"))
    return yell_cache[curr]


def find(humn):
    yell_cache = {}
    monkeys["humn"] = humn
    return yell_root_diff("root", yell_cache)


lower = int(-1e20)
upper = int(1e20)
while True:
    humn_to_try = int((lower + upper) / 2)
    res = find(humn_to_try)
    if res == 0:
        break
    res_lower = find(lower)
    if res * res_lower < 0:
        upper = humn_to_try
    else:
        lower = humn_to_try

print(f"Part 2: {humn_to_try - 1}")
