from pathlib import Path

lines = Path("input.txt").read_text().splitlines()

scratches = {}
card = 1
for line in lines:
    line = line.split(": ")[1]
    winning = [int(x) for x in line.split(" | ")[0].split(" ") if x != ""]
    nbrs = [int(x) for x in line.split(" | ")[1].split(" ") if x != ""]
    scratches[card] = (winning, nbrs)
    card += 1

point_tot = 0
for card, (winning, nbrs) in scratches.items():
    points = 0
    for nbr in nbrs:
        if nbr in winning:
            if points == 0:
                points = 1
            else:
                points *= 2

    point_tot += points

print(f"Part 1: {point_tot}")


cards = {}
copies = {}
index = 0
for card, (winning, nbrs) in scratches.items():
    cards.setdefault(card, 0)
    cards[card] += 1

    points = 0
    for nbr in nbrs:
        if nbr in winning:
            points += 1

    next_cards = list(scratches.keys())[index+1:index+1+points]
    for next_card in next_cards:
        copies.setdefault(next_card, 0)
        copies[next_card] += 1 

    if card in copies:
        for i in range(copies[card]):
            for next_card in next_cards:
                copies[next_card] += 1 

    index += 1

tot_cards = {}
for card, count in cards.items():
    tot_cards.setdefault(card, 0)
    tot_cards[card] += count

for card, count in copies.items():
    tot_cards.setdefault(card, 0)
    tot_cards[card] += count

print(f"Part 2: {sum(tot_cards.values())}")

