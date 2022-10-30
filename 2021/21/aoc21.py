from pathlib import Path

positions = [int(x.strip().split(" ")[-1]) - 1 for x in Path("input.txt").open("r").readlines()]
scores = [0, 0]
die = [x for x in range(1, 101)]
board = [x for x in range(1, 11)]
die_index = 0
die_cnt = 0


def roll_die():
    global die_index, die_cnt
    val = die[die_index]
    die_index += 1
    die_index %= len(die)
    die_cnt += 1
    return val


def play_round(player):
    move = roll_die() + roll_die() + roll_die()
    positions[player] = (positions[player] + move) % len(board)
    scores[player] += board[positions[player]]
    return scores[player] >= 1000


loser = -1
while True:
    if play_round(0):
        loser = 1
        break
    if play_round(1):
        loser = 0
        break


print(f"Part 1: {scores[loser] * die_cnt}")


def play_dirac(pos0, pos1, curr_score0, curr_score1, turn):
    if curr_score0 >= 21:
        return 1, 0

    if curr_score1 >= 21:
        return 0, 1

    all_branch_wins = (0, 0)
    if turn == 0:
        for i, cnt in [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]:
            next_pos = (pos0 + i) % len(board)
            branch_wins = play_dirac(next_pos, pos1, curr_score0 + board[next_pos], curr_score1, 1)
            all_branch_wins = (all_branch_wins[0] + branch_wins[0] * cnt, all_branch_wins[1] + branch_wins[1] * cnt)
    else:
        for i, cnt in [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]:
            next_pos = (pos1 + i) % len(board)
            branch_wins = play_dirac(pos0, next_pos, curr_score0, curr_score1 + board[next_pos], 0)
            all_branch_wins = (all_branch_wins[0] + branch_wins[0] * cnt, all_branch_wins[1] + branch_wins[1] * cnt)

    return all_branch_wins


positions = [int(x.strip().split(" ")[-1]) - 1 for x in Path("input.txt").open("r").readlines()]
res = play_dirac(positions[0], positions[1], 0, 0, 0)
print(f"Part 2: {max(*res)}")

# 1 1 1 = 3
# 1 1 2 = 4
# 1 1 3 = 5
# 1 2 1 = 4
# 1 2 2 = 5
# 1 2 3 = 6
# 1 3 1 = 5
# 1 3 2 = 6
# 1 3 3 = 7
# 2 1 1 = 4
# 2 1 2 = 5
# 2 1 3 = 6
# 2 2 1 = 5
# 2 2 2 = 6
# 2 2 3 = 7
# 2 3 1 = 6
# 2 3 2 = 7
# 2 3 3 = 8
# 3 1 1 = 5
# 3 1 2 = 6
# 3 1 3 = 7
# 3 2 1 = 6
# 3 2 2 = 7
# 3 2 3 = 8
# 3 3 1 = 7
# 3 3 2 = 8
# 3 3 3 = 9
