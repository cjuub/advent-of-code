input = '165061'
input_list = list(input)
recipes = '37'

scores = list(recipes)
elves = [0, 1]

str_scores = '37'
orig_len = int(input)
# while len(scores) < orig_len + 10: # part 1
while True:
    score = 0
    curr_scores = []
    for j in range(len(elves)):
        curr_score = int(scores[elves[j] % len(scores)])
        score += curr_score
        curr_scores.append(curr_score)
    scores += list(str(score))
    for j in range(len(elves)):
        elves[j] = (elves[j] + curr_scores[j] + 1) % len(scores)


    last_scores = scores[len(scores) - len(input):]
    last_scores_prev = scores[len(scores) - len(input) - 1:-1]

    if last_scores == input_list or last_scores_prev == input_list:
        break


# part 1
# print(scores)
# print(str(''.join(scores[orig_len:orig_len+10])))
# print()

print(''.join(scores[:-len(input)]))
if last_scores == input_list:
    print(len(''.join(scores[:-len(input)])))
else:
    print(len(''.join(scores[:-len(input) - 1])))
