from pathlib import Path

lines = [x.strip() for x in Path("input.txt").open("r").readlines()]

snafus = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}

tot = 0
for line in lines:
    dec = 0
    for i, d in enumerate(line):
        dec += (5 ** (len(line) - i - 1)) * snafus[d]

    tot += dec

reverse_snafus = {
    0: "0",
    1: "1",
    2: "2",
    3: "=",
    4: "-",
    5: "0",
}

snafu = ""
carry = 0
while tot != 0 or carry > 0:
    x = tot % 5 + carry
    snafu = reverse_snafus[x] + snafu
    carry = 0
    if x > 2:
        carry = 1

    tot = int(tot / 5)

print(f"Part 1: {snafu}")
