import enum
from pathlib import Path
from typing import OrderedDict

class CardType(enum.IntEnum):
    C2 = 0
    C3 = 1
    C4 = 2
    C5 = 3
    C6 = 4
    C7 = 5
    C8 = 6
    C9 = 7
    T = 8
    J = 9
    Q = 10
    K = 11
    A = 12

class HandType(enum.IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6

def get_hand_type(hand):
    hand_type = HandType.HIGH_CARD
    for card in hand:
        if hand.count(card) >= 2:
            hand_type = HandType.ONE_PAIR

    for card1 in hand:
        has_card1_pair = hand.count(card1) >= 2
        for card2 in hand:
            if card1 == card2:
                continue

            if hand.count(card2) >= 2:
                if has_card1_pair:
                    hand_type = HandType.TWO_PAIR

    for card in hand:
        if hand.count(card) >= 3:
            hand_type = HandType.THREE_OF_A_KIND

    if hand_type == HandType.THREE_OF_A_KIND:
        for card in hand:
            if hand.count(card) == 2:
                hand_type = HandType.FULL_HOUSE

    for card in hand:
        if hand.count(card) >= 4:
            hand_type = HandType.FOUR_OF_A_KIND

    for card in hand:
        if hand.count(card) >= 5:
            hand_type = HandType.FIVE_OF_A_KIND

    return hand_type

def get_hand(hand_str, bid, CT):
    hand = []
    for card in hand_str:
        if card == "2":
            hand.append(CT.C2)
        elif card == "3":
            hand.append(CT.C3)
        elif card == "4":
            hand.append(CT.C4)
        elif card == "5":
            hand.append(CT.C5)
        elif card == "6":
            hand.append(CT.C6)
        elif card == "7":
            hand.append(CT.C7)
        elif card == "8":
            hand.append(CT.C8)
        elif card == "9":
            hand.append(CT.C9)
        elif card == "T":
            hand.append(CT.T)
        elif card == "J":
            hand.append(CT.J)
        elif card == "Q":
            hand.append(CT.Q)
        elif card == "K":
            hand.append(CT.K)
        elif card == "A":
            hand.append(CT.A)

    hand_type = get_hand_type(hand)

    return hand, hand_type, bid


lines = Path("input.txt").read_text().splitlines()

hand_type_mapper = OrderedDict({
    HandType.HIGH_CARD: [],
    HandType.ONE_PAIR: [],
    HandType.TWO_PAIR: [],
    HandType.THREE_OF_A_KIND: [],
    HandType.FULL_HOUSE: [],
    HandType.FOUR_OF_A_KIND: [],
    HandType.FIVE_OF_A_KIND: [],
})

hands = []
for line in lines:
    hand_str = line.split(" ")[0]
    bid = int(line.split(" ")[1])

    hand, hand_type, bid = get_hand(hand_str, bid, CardType)
    hands.append((hand, hand_type, bid))
    hand_type_mapper[hand_type].append(hands[-1])



rank = 0
tot = 0
for hand_type, hands in hand_type_mapper.items():
    hands.sort(key = lambda x: x[0], reverse=False)

    for hand, _, bid in hands:
        rank += 1
        tot += bid * rank

print(f"Part 1: {tot}")



class CardType2(enum.IntEnum):
    J = -1
    C2 = 0
    C3 = 1
    C4 = 2
    C5 = 3
    C6 = 4
    C7 = 5
    C8 = 6
    C9 = 7
    T = 8
    Q = 10
    K = 11
    A = 12


hands = []
for line in lines:
    hand_str = line.split(" ")[0]
    bid = int(line.split(" ")[1])

    hand, hand_type, bid = get_hand(hand_str, bid, CardType2)
    hands.append((hand, hand_type, bid))


def find_best_hand(hand, curr_best):
    new_hand_type = get_hand_type(hand)
    if new_hand_type > curr_best[0]:
        curr_best[0] = new_hand_type

    for i, card in enumerate(hand):
        if card != CardType2.J:
            continue

        for card2 in CardType2:
            if card2 == CardType2.J:
                continue
            new_hand = hand[:]
            new_hand[i] = card2
            find_best_hand(new_hand, curr_best)

hand_type_mapper = OrderedDict({
    HandType.HIGH_CARD: [],
    HandType.ONE_PAIR: [],
    HandType.TWO_PAIR: [],
    HandType.THREE_OF_A_KIND: [],
    HandType.FULL_HOUSE: [],
    HandType.FOUR_OF_A_KIND: [],
    HandType.FIVE_OF_A_KIND: [],
})

new_hands = []
for hand, hand_type, bid in hands:
    new_hand = hand[:]
    new_hand_type = [hand_type]
    find_best_hand(hand, new_hand_type)
    if new_hand_type[0] > hand_type:
        hand_type = new_hand_type[0]

    new_hands.append((hand, hand_type, bid))
    hand_type_mapper[hand_type].append(new_hands[-1])


rank = 0
tot = 0
for hand_type, hands in hand_type_mapper.items():
    hands.sort(key = lambda x: x[0], reverse=False)

    for hand, _, bid in hands:
        rank += 1
        tot += bid * rank

print(f"Part 2: {tot}")
