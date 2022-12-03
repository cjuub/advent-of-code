from pathlib import Path

rounds = [x.strip().split(" ") for x in Path("input.txt").open("r").readlines()]

shape_score_map = {"X": 1, "Y": 2, "Z": 3}
outcome_score_map = {"AX": 3, "AY": 6, "AZ": 0,
                     "BX": 0, "BY": 3, "BZ": 6,
                     "CX": 6, "CY": 0, "CZ": 3}
to_win_score_map = {"AX": 0, "AY": 3, "AZ": 6,
                    "BX": 0, "BY": 3, "BZ": 6,
                    "CX": 0, "CY": 3, "CZ": 6}
choice_map = {"X": {"A": "Z", "B": "X", "C": "Y"},
              "Y": {"A": "X", "B": "Y", "C": "Z"},
              "Z": {"A": "Y", "B": "Z", "C": "X"}}

score = 0
for opponent, you in rounds:
    score += shape_score_map[you] + outcome_score_map[opponent + you]

print(f"Part 1: {score}")

score = 0
for opponent, you in rounds:
    score += shape_score_map[choice_map[you][opponent]] + to_win_score_map[opponent + you]

print(f"Part 2: {score}")
