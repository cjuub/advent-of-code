from pathlib import Path

lines = Path("input.txt").read_text().splitlines()

histories = []
for line in lines:
    histories.append([int(x) for x in line.split(" ")])

def find_sequences(history, left_index, right_index, depth, sequence, sequences):

    diff = history[right_index] - history[left_index]
    sequence.append(diff)

    if right_index == len(history) - 1:
        sequences.append(sequence)
        if all([x == 0 for x in sequence]):
            return

        find_sequences(sequence[:], 0, 1, depth + 1, [], sequences)
        return

    find_sequences(history, left_index + 1, right_index + 1, depth, sequence, sequences)

def extrapolate(history, sequences) -> int:
    new_val = 0
    reversed_sequences = list(reversed(sequences))
    for i, sequence in enumerate(reversed_sequences):
        sequence.append(new_val)
        if i + 1 == len(sequences):
            return history[-1] + new_val
        else:
            new_val = reversed_sequences[i + 1][-1] + new_val

    raise Exception()

tot = 0
for history in histories:
    sequences = []
    find_sequences(history, 0, 1, 0, [], sequences)
    new_val = extrapolate(history, sequences)
    tot += new_val

print(f"Part 1: {tot}")

def extrapolate2(history, sequences) -> int:
    new_val = 0
    reversed_sequences = list(reversed(sequences))
    for i, sequence in enumerate(reversed_sequences):
        sequence.insert(0, new_val)
        if i + 1 == len(sequences):
            return history[0] - new_val
        else:
            new_val = reversed_sequences[i + 1][0] - new_val

    raise Exception()

tot = 0
for history in histories:
    sequences = []
    find_sequences(history, 0, 1, 0, [], sequences)
    new_val = extrapolate2(history, sequences)
    tot += new_val

print(f"Part 2: {tot}")

