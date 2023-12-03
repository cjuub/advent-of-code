from pathlib import Path

lines = Path("input.txt").read_text().splitlines()

games = {}
for line in lines:
    game = int(line.split(": ")[0].split(" ")[1])
    bags_split = line.split(": ")[1].split("; ")
    bags = []
    for bag in bags_split:
        red = 0
        green = 0
        blue = 0
        for val in bag.split(", "):
            if val.endswith("red"):
                red = int(val.split(" ")[0])
            elif val.endswith("green"):
                green = int(val.split(" ")[0])
            elif val.endswith("blue"):
                blue = int(val.split(" ")[0])
            else:
                assert False

        bags.append((red, green, blue))
    games[game] = bags

sum = 0
for game, bags in games.items():
    bad = False
    for red, green, blue in bags:
        reds = 12
        greens = 13
        blues = 14
        reds -= red
        greens -= green
        blues -= blue

        if reds < 0 or greens < 0 or blues < 0:
            bad = True
    if not bad:
        sum += game

print(f"Part 1: {sum}")


sum = 0
for game, bags in games.items():

    best_red = 0
    for min_red in range(100):
        bad = False
        for red, green, blue in bags:
            if min_red - red < 0:
                bad = True
                break

        if not bad:
            best_red = min_red
            break

    best_green = 0
    for min_green in range(100):
        bad = False
        for red, green, blue in bags:
            if min_green - green < 0:
                bad = True
                break

        if not bad:
            best_green = min_green
            break

    best_blue = 0
    for min_blue in range(100):
        bad = False
        for red, green, blue in bags:
            if min_blue - blue < 0:
                bad = True
                break
        if not bad:
            best_blue = min_blue
            break

    power = best_red * best_green * best_blue
    assert power != 0, f"{game} {best_red} {best_green} {best_blue}"
    sum += power

print(f"Part 2: {sum}")
